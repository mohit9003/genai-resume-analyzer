import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import google.generativeai as genai
import re

# ---------- LOAD ENV ----------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ API Key not found")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-flash-latest")

# ---------- PAGE ----------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🚀", layout="wide")

# ---------- CSS ----------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
h1, h2, h3 {
    text-align: center;
}
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #06b6d4);
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1>🚀 Smart AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>AI-powered resume scoring + career assistant</p>", unsafe_allow_html=True)

# ---------- ROLES ----------
roles = [
    "Software Engineer",
    "Data Analyst",
    "Machine Learning Engineer",
    "Data Scientist",
    "Web Developer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "DevOps Engineer",
    "Cyber Security Analyst",
    "Cloud Engineer",
    "UI/UX Designer",
    "Product Manager"
]

# ---------- LAYOUT ----------
col1, col2 = st.columns(2)

with col1:
    role = st.selectbox("🎯 Select Job Role", roles)

with col2:
    uploaded_file = st.file_uploader("📄 Upload Resume", type="pdf")

# ---------- PDF EXTRACT ----------
def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

# ---------- TABS ----------
tab1, tab2 = st.tabs(["📊 Resume Analysis", "🤖 AI Chat"])

# ---------- ANALYSIS ----------
with tab1:
    if uploaded_file:
        resume_text = extract_text(uploaded_file)

        if st.button("🚀 Analyze Resume"):
            with st.spinner("Analyzing with AI..."):

                prompt = f"""
                Analyze this resume for {role} role and return:

                1. Key Skills
                2. Missing Skills
                3. Suggestions
                4. ATS Score out of 100 (just number)

                Resume:
                {resume_text}
                """

                response = model.generate_content(prompt)
                result = response.text

                # Extract score
                score_match = re.search(r'\b\d{1,3}\b', result)
                score = int(score_match.group()) if score_match else 50

                st.success("✅ Analysis Complete")

                # Score UI
                st.subheader("📈 Resume Score")
                st.progress(score / 100)
                st.write(f"**Score: {score}/100**")

                # Output
                st.markdown("### 📊 Detailed Analysis")
                st.write(result)

                # Download
                st.download_button(
                    "📥 Download Report",
                    result,
                    file_name="resume_analysis.txt"
                )
    else:
        st.info("📌 Upload a resume to start analysis")

# ---------- CHAT ----------
st.markdown("""
<style>
.chat-nav {
    position: fixed;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-nav">', unsafe_allow_html=True)

if st.button("💬 Chat AI"):
    st.switch_page("chat")

st.markdown('</div>', unsafe_allow_html=True)


# ---------- RESUME RESOURCES ----------
st.markdown("---")
st.markdown("## 📁 Resume Resources")

tab3, tab4 = st.tabs(["📄 Resume Template", "📌 Resume Example"])

# ---------- TEMPLATE ----------
with tab3:
    st.subheader("📄 Professional Resume Template")
    st.image("images/template.png", use_container_width=True)

    st.info("💡 Use this clean template to build an ATS-friendly resume")

# ---------- EXAMPLE ----------
with tab4:
    st.subheader("📌 Sample Resume Example")
    st.image("images/example.png", use_container_width=True)

    st.info("💡 Follow this example to structure your resume effectively")