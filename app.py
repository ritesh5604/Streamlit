import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF for PDF processing
import io  # For handling PDF bytes

# Streamlit App UI
st.set_page_config(page_title="Reverse Job Interview AI", page_icon="💼", layout="wide")

# Google Gemini API Setup
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_pdf):
    """Extract text from a PDF file uploaded via Streamlit."""
    text = ""
    with fitz.open(stream=uploaded_pdf.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text.strip()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit Title
st.title("💼 Reverse Job Interview AI - Know Your Worth")
st.write("Empower job seekers with AI-driven insights on employers!")

# PDF Upload Section
st.subheader("📂 Upload Job Description (PDF)")
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
job_description = ""

if pdf_file is not None:
    try:
        job_description = extract_text_from_pdf(pdf_file)
        st.text_area("📝 Extracted Job Description:", job_description, height=200, disabled=True)
    except Exception as e:
        st.error(f"❌ Error reading PDF: {str(e)}")

# Alternative Manual Input
st.subheader("📝 Or Paste Job Description Below")
manual_input = st.text_area("Paste Job Description:", height=200)

# Prioritize manual input over PDF text
if manual_input.strip():
    job_description = manual_input.strip()

# Job Description Analysis
if st.button("🔍 Analyze Job Description"):
    if job_description:
        with st.spinner("Analyzing job description..."):
            try:
                prompt = f"""
                Analyze the following job description and provide a text-based summary with insights. 
                Focus on key details like job title, company, salary transparency, and potential red flags 
                related to work-life balance, unrealistic expectations, or toxic culture.

                Job Description: {job_description}
                """
                
                response = model.generate_content(prompt)
                ai_analysis = response.text if hasattr(response, "text") else "⚠️ AI response could not be retrieved."
                
                # Display text-based output instead of JSON
                st.subheader("📊 AI Analysis")
                st.write(ai_analysis)
                
            except Exception as e:
                st.error(f"❌ Error generating AI response: {str(e)}")
    else:
        st.warning("⚠️ Please enter or upload a job description first!")

# AI Chatbot Section
st.subheader("🤖 AI Interview Chatbot")
user_input = st.text_input("💬 Ask for interview tips, salary negotiation strategies, or company insights:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)
    
    try:
        response = model.generate_content(user_input)
        ai_reply = response.text if hasattr(response, "text") else "⚠️ AI response could not be retrieved."
    except Exception as e:
        ai_reply = f"❌ Error generating response: {str(e)}"
    
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    
    with st.chat_message("assistant"):
        st.write(ai_reply)

# Chat History Section
st.subheader("📝 Chat History")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
