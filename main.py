import os
import sys
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# ==========================================================
# 🔍 PATH & KEY CHECKING (Verified working!)
# ==========================================================
script_dir = Path(__file__).resolve().parent
env_path = script_dir / ".env"

load_dotenv(dotenv_path=env_path)

mistral_key = os.getenv("MISTRAL_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")

if not tavily_key or not mistral_key:
    print("❌ CRITICAL ERROR: Keys are missing!")
    sys.exit(1)

# Universal LangChain Imports
from langchain_core.tools import tool
from langchain_mistralai import ChatMistralAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage

# ==========================================
# PHASE 1: CREATE THE FREE TOOLS
# ==========================================

@tool
def scrape_website_tool(url: str) -> str:
    """Useful when you need to read and extract text from a specific company website URL."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read()
            
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        
        return soup.get_text(separator=" ")[:4000]
    except Exception as e:
        return f"Could not scrape website. Error: {str(e)}"

# Setup Tavily search tool explicitly passing the verified key
free_tavily_search_tool = TavilySearchResults(max_results=3, tavily_api_key=tavily_key)
my_tools = [scrape_website_tool, free_tavily_search_tool]


# ==========================================
# PHASE 2: DEFINE THE BROCHURE STRUCTURE
# ==========================================

class BrochureStructure(BaseModel):
    company_name: str = Field(description="The name of the business.")
    headline: str = Field(description="A catchy, attractive marketing header.")
    about: str = Field(description="A summary introduction of what the company does.")
    features: list[str] = Field(description="A list of 3 major products, features, or services.")
    call_to_action: str = Field(description="Instructions on what the reader should do next.")


# ==========================================
# PHASE 3: RUN THE AGENT AND FORMATTER
# ==========================================

def run_generator(target_url: str):
    print("🤖 Mistral + Tavily Agent is starting up via UV...")
    
    # Initialize the Mistral model and bind your tools to it directly
    llm = ChatMistralAI(model="mistral-large-latest", temperature=0.5, mistral_api_key=mistral_key)
    model_with_tools = llm.bind_tools(my_tools)
    
    system_instruction = (
        "You are an expert marketing agent. Your task is to gather data about a company and write a beautiful brochure. "
        "Use your tools (scrape_website_tool or TavilySearchResults) to discover info if needed."
    )
    user_prompt = f"Please research the company at this URL and create a copy draft layout for a brochure: {target_url}"
    
    # We construct an explicit chat message history sequence
    messages = [
        SystemMessage(content=system_instruction),
        HumanMessage(content=user_prompt)
    ]
    
    initial_response = model_with_tools.invoke(messages)
    raw_text_result = initial_response.content
    
    # Resolve tool contents using Mistral's required strict request-response ordering
    if initial_response.tool_calls:
        print("🛠️ Agent is interacting with tools to extract company details...")
        
        # 1. We MUST append the assistant's request message containing the tool calls first
        messages.append(initial_response)
        
        # 2. We execute each tool call and immediately append its corresponding ToolMessage wrapper
        for tool_call in initial_response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]
            
            if tool_name == "scrape_website_tool":
                output = scrape_website_tool.invoke(tool_args)
            elif tool_name == "TavilySearchResults":
                output = str(free_tavily_search_tool.invoke(tool_args))
            else:
                output = "Tool not found."
                
            # Append the direct structural response to fulfill API message parity
            messages.append(ToolMessage(content=output, tool_call_id=tool_id))
                
        print(f"📝 Retracted text processing completed. Resolving finalized brochure layout...")
        
        # Send back the clean history containing tool pairs back to Mistral
        final_text_response = llm.invoke(messages)
        raw_text_result = final_text_response.content

    print("✨ Formatting text into structured brochure layout schema...")
    structuring_llm = llm.with_structured_output(BrochureStructure)
    clean_brochure = structuring_llm.invoke(f"Format this text into the schema:\n\n{raw_text_result}")
    
    return clean_brochure

if __name__ == "__main__":
    company_link = input("enter the comapny name or link ") 
    
    final_result = run_generator(company_link)
    
    print("\n====================================")
    print(f"🏢 COMPANY: {final_result.company_name}")
    print(f"📢 HEADLINE: {final_result.headline}")
    print(f"📖 ABOUT:\n{final_result.about}")
    print("🛠️ TOP OFFERINGS:")
    for feature in final_result.features:
        print(f"  • {feature}")
    print(f"📞 NEXT STEPS: {final_result.call_to_action}")
    print("====================================")
