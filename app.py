import os
import streamlit as st
import PyPDF2
import google.generativeai as genai

# -------------------------------
# 1. Setup Google Gemini API Key
# -------------------------------
GEMINI_API_KEY = "your_gemini_api_key_here"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

# -------------------------------
# 2. Streamlit UI
# -------------------------------
st.set_page_config(page_title="📊 AI Bank Statement Analyzer", page_icon="🏦", layout="wide")

# Custom Title + Subtitle
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🏦 AI-Powered Bank & UPI Statement Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Upload your ePassbook or UPI PDF statement to get instant financial insights</p>", unsafe_allow_html=True)

# Sidebar instructions
st.sidebar.title("ℹ️ How to Use This Tool")
st.sidebar.write("""
- Upload your **Bank Statement (ePassbook)** or **UPI Statement PDF**.  
- The AI will extract and analyze **all transactions** (not just UPI).  
- You’ll get insights like:
  - Income vs Expenses  
  - Spending patterns  
  - Savings rate  
  - Categories where you should cut down or can spend more  

### 🏦 How to Download Your Statement:
Open your bank’s mobile banking app (Example:  
- *Canara Bank → Canara ai1*  
- *Bank of Baroda → BOB World*  
- *SBI → YONO SBI*  
)  
Download the **PDF Statement** for the period you want to analyze.
""")

# -------------------------------
# File Uploader
# -------------------------------
uploaded_file = st.file_uploader("📂 Upload Bank/UPI Statement PDF", type=["pdf"])

# -------------------------------
# PDF Text Extractor
# -------------------------------
def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file using PyPDF2"""
    text = ""
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text.strip()

# -------------------------------
# Validate Statement
# -------------------------------
def validate_statement(text):
    """Ask Gemini if the text looks like a Bank/UPI statement"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are a validator. Check if the following text is a **bank statement or UPI statement**.
    If YES → reply with only "VALID".
    If NO → reply with only "INVALID".
    
    Text:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# -------------------------------
# Analyze Financial Data with Gemini
# -------------------------------
def analyze_financial_data(text, filename):
    """Sends extracted text to Gemini for financial analysis"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are a financial advisor AI. Analyze the following **bank statement (not just UPI)**:

    {text}

    Provide insights in this format:
    **Financial Insights for {filename}**
    - **Total Income**: ₹[amount]
    - **Total Expenses**: ₹[amount]
    - **Savings**: ₹[amount] ([percentage] %)
    - **Top Spending Categories**: [category: amount]
    - **Category-wise Summary**: [Food: ₹x, Travel: ₹y, Shopping: ₹z, etc.]
    - **Time-based Spending Trends**: [monthly or weekly breakdown if visible]
    - **Wasteful Transactions Detected**: [list suspicious/unnecessary spends]
    - **Spending Patterns**: [short overall summary of habits]
    - **Recommendations**: [advice for budgeting, where to minimize, where spending is healthy]
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response else "⚠️ Couldn’t generate insights."

# -------------------------------
# Main Flow
# -------------------------------
if uploaded_file is not None:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File uploaded successfully!")

    with st.spinner("📄 Extracting text from your statement..."):
        extracted_text = extract_text_from_pdf(file_path)

    if not extracted_text:
        st.error("⚠️ Could not extract text. Please upload a **digital statement PDF** (not scanned image).")
    else:
        # Validate first
        validation = validate_statement(extracted_text)

        if "INVALID" in validation.upper():
            st.error("⚠️ This is not a valid Bank or UPI statement. Please follow the guidelines in the menu bar and upload the correct PDF.")
        else:
            with st.spinner("🧠 Analyzing your financial data with AI..."):
                insights = analyze_financial_data(extracted_text, uploaded_file.name)

            st.subheader("📊 Financial Insights Report")
            st.write(insights)

            st.markdown('<div style="background: linear-gradient(to right, #2E7D32, #1B5E20); color: white; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold;">✅ Analysis Completed! Use these insights to manage your money wisely 🚀</div>', unsafe_allow_html=True)

    os.remove(file_path)
