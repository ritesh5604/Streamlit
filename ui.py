import streamlit as st
import PyPDF2

# Streamlit UI Setup
st.set_page_config(page_title="Job Scanner AI", page_icon="📄", layout="wide")

st.title("📄 Job Scanner AI")
st.write("Upload a job description file 📎 or paste text manually to analyze.")

# Custom styling for the upload icon inside text area
st.markdown(
    """
    <style>
        .file-upload {
            position: absolute;
            right: 10px;
            top: 10px;
            font-size: 20px;
            cursor: pointer;
            color: #007bff;
        }
        .file-upload:hover {
            color: #0056b3;
        }
        .stTextArea textarea {
            padding-right: 40px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# File Upload Button
uploaded_file = st.file_uploader("📎 Upload", type=["pdf", "txt"])

# Job Description Input
job_description = st.text_area("Paste Job Description:", height=200)

# If a file is uploaded, extract text and fill the text area
if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "txt":
        job_description = uploaded_file.read().decode("utf-8")
    elif file_type == "pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        job_description = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    
    st.success("✅ File uploaded successfully! Text extracted.")

# Analyze Button
if st.button("🔍 Scan & Analyze"):
    if job_description.strip():
        st.success("✅ Text received! (Processing... 🔄)")
        # Add AI analysis logic here
    else:
        st.warning("⚠️ Please upload a file or enter text manually!")

