import streamlit as st
from main import run_generator

st.set_page_config(
    page_title="AI Brochure Generator",
    page_icon="📄",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main{
    background:#F5F7FA;
}

.block-container{
    padding-top:2rem;
}

.title{
    text-align:center;
    font-size:48px;
    font-weight:700;
    color:#1E3A8A;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:18px;
    margin-bottom:30px;
}

div[data-testid="stTextInput"] input{
    border-radius:12px;
    border:2px solid #4F46E5;
    padding:10px;
}

div.stButton > button{
    width:100%;
    background:#4F46E5;
    color:white;
    border-radius:10px;
    height:55px;
    font-size:18px;
    border:none;
}

div.stButton > button:hover{
    background:#4338CA;
}

.card{
    background:white;
    padding:25px;
    border-radius:15px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
    margin-top:20px;
}

.feature{
    background:#EEF2FF;
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:50px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("<div class='title'>📄 AI Brochure Generator</div>", unsafe_allow_html=True)

st.markdown(
"""
<div class='subtitle'>
Generate beautiful AI-powered marketing brochures from any company website.
</div>
""",
unsafe_allow_html=True)

# ---------------- INPUT ----------------

url = st.text_input(
    "🌐 Company Website",
    placeholder="https://www.spacex.com"
)

generate = st.button("🚀 Generate Brochure")

# ---------------- OUTPUT ----------------

if generate:

    if url == "":
        st.warning("Please enter a website URL.")
        st.stop()

    with st.spinner("🤖 AI is researching the company..."):
        brochure = run_generator(url)

    st.success("Brochure Generated Successfully!")

    st.markdown("---")

    st.markdown(
        f"""
        <div class='card'>
        <h1>{brochure.company_name}</h1>
        <h3 style='color:#4F46E5'>{brochure.headline}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([2,1])

    with col1:

        st.markdown(
        f"""
        <div class='card'>
        <h2>📖 About</h2>
        <p>{brochure.about}</p>
        </div>
        """,
        unsafe_allow_html=True
        )

    with col2:

        st.markdown(
        """
        <div class='card'>
        <h2>⭐ Top Features</h2>
        """,
        unsafe_allow_html=True
        )

        for feature in brochure.features:
            st.markdown(
                f"<div class='feature'>✔ {feature}</div>",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
    f"""
    <div class='card'>
    <h2>📞 Call To Action</h2>
    <p style='font-size:18px;'>{brochure.call_to_action}</p>
    </div>
    """,
    unsafe_allow_html=True
    )

st.markdown(
"""
<div class='footer'>
Made with ❤️ using Streamlit + Mistral AI
</div>
""",
unsafe_allow_html=True)