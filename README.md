# AI_Personal_UPI_Usage_and_Financial_Analyzer  

An interactive **Streamlit-based financial analyzer** that extracts and analyzes transactions from **Bank ePassbook statements** or **UPI transaction PDFs**, using **PyPDF2** for text extraction and **Google Gemini AI** for insights.  

---

## 🔍 Project Overview  

### ✅ Data Source:  
- 📄 Input: Bank Statement PDFs (e.g., ePassbook, UPI transaction history)  
- Format: `.pdf` (must be a **digital statement**, not scanned image)  
- Example sources:  
  - *Canara Bank → Canara ePassbook*  
  - *Bank of Baroda → BOB World*  
  - *SBI → YONO SBI*  

---

## ⚙️ PDF Processing & Validation  

### 📂 PDF Extraction  
- Uses **PyPDF2** to read PDF pages and extract raw text.  

```python
reader = PyPDF2.PdfReader(pdf_file)
for page in reader.pages:
    text += page.extract_text()
```
## ✅ Statement Validation  

- AI checks whether the uploaded document is a **valid Bank/UPI statement**.  
- If invalid (e.g., random PDF like a brochure/design brief), it shows a polite error:  

> ⚠️ *“This is not a valid Bank or UPI Statement. Please follow the guidelines in the menu and upload a proper statement PDF.”*  

---

## 🤖 Financial Analysis with Gemini  

### 🔧 Tasks Performed by Gemini AI  

#### 📑 Transaction Parsing  
Extracts transactions into structured fields:  
- **Date**  
- **Time** (if present)  
- **Description**  
- **Txn_Type** (Debit/Credit)  
- **Amount**  
- **Balance** (if present)  

#### 📊 Financial Insights  
- **Total Income & Expenses**  
- **Savings** (amount + percentage)  
- **Spending Patterns**  
  - ⏳ *Time-based trends*  
  - 📂 *Category-wise summaries*  
- **Wasteful Transaction Detection**  
- **Budgeting Recommendations**  

---

## 🚀 Streamlit Application: `app.py`  

### 🔧 Features  

#### 1️⃣ Upload & Validation  
- Upload **Bank/UPI PDF statement**  
- Automatic validation of file type  

#### 2️⃣ Extraction  
- Extracts text from PDF via **PyPDF2**  
- Rejects **scanned PDFs** (since no text is extractable)  

#### 3️⃣ AI Analysis  
- Sends text to **Google Gemini (gemini-1.5-flash)**  
- Returns **structured financial insights**  

#### 4️⃣ Output Display  
- 📑 **Transaction DataFrame** (preview of extracted transactions)  
- 📊 **Financial Insights Report** with:  
  - Income vs Expenses  
  - Savings & trends  
  - Category-wise breakdown  
  - Recommendations  
## 💻 How to Run This Project
### 🧪 Step 1: Create Virtual Environment
```bash
python -m venv env_name
```
### ▶️ Step 2: Activate Environment
#### Windows
```bash
.\env_name\Scripts\activate
```
#### macOS/Linux
```bash
source env_name/bin/activate
```
### 📦 Step 3: Install Dependencies
```bash
pip install streamlit PyPDF2 google-generativeai
```
### 🔑 Step 4: Setup Google Gemini API Key
#### GOOGLE_API_KEY="your_gemini_api_key_here"  
#generate your api key from https://aistudio.google.com/app/apikey and paste it here
### 🚀 Step 5: Run Streamlit App
```bash
streamlit run app.py
```
## 📌 Example Insights
### 📊 Financial Insights for statement.pdf
- Total Income: ₹60,000
- Total Expenses: ₹45,000
- Savings: ₹15,000 (25%)
- Top Spending Categories: Food ₹12,000, Travel ₹8,000, Shopping ₹7,000
- Time-based Spending Trend: Higher spends on weekends
- Wasteful Transactions: Frequent online food delivery orders
- Recommendations: Reduce online food orders, maintain savings discipline

