# 🚀 AI Brochure Generator

Turn any website into a professional marketing brochure in seconds using AI.

Instead of spending hours reading through a website and writing promotional content, this application analyzes the website, understands its purpose, and generates a clear, engaging brochure automatically.

Whether it's a startup, business, or personal portfolio, the AI creates content that is ready to present or further customize.

---

## ✨ What It Does

- Accepts a website URL as input
- Extracts and cleans website content
- Uses AI to understand the business
- Generates a professional marketing brochure
- Displays the brochure through a clean Streamlit interface

---

## 🛠 Built With

- Python
- Streamlit
- LangChain
- Mistral AI
- Tavily Search API
- BeautifulSoup
- Requests
- Python Dotenv

---

## ⚡ How It Works

```
Website URL
     │
     ▼
Extract Website Content
     │
     ▼
Clean & Process Information
     │
     ▼
Enhance Context with Tavily Search
     │
     ▼
Generate Brochure using Mistral AI
     │
     ▼
Display Final Brochure
```

---

## 📂 Project Structure

```
AI-Brochure-Generator/
│
├── app.py
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/your-username/AI-Brochure-Generator.git
cd AI-Brochure-Generator
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
MISTRAL_API_KEY=your_api_key
TAVILY_API_KEY=your_api_key
```

### Run the application

```bash
streamlit run app.py
```

---

## 💡 Why I Built This

Writing marketing content for websites is often repetitive and time-consuming.

I wanted to explore how Large Language Models can automate this process by combining web scraping, search, and AI into a single workflow. This project helped me gain hands-on experience with LangChain, prompt engineering, API integration, and building AI-powered applications.

---

## 🎯 Key Learnings

During this project, I worked with:

- Large Language Models (LLMs)
- LangChain
- Prompt Engineering
- Web Scraping
- API Integration
- Streamlit
- AI Content Generation

---

## 🔮 Future Improvements

- Export brochures as PDF
- Multiple brochure templates
- Multi-language support
- Brand-specific customization
- AI-generated images
- Improved formatting and styling

---

## ⭐ Support

If you found this project useful or interesting, consider giving it a **Star**. It helps others discover the project and motivates me to build more AI applications.

---

## 👨‍💻 Author

**Sameer Anand**

*Learning, building, and experimenting with AI one project at a time.*
