# 🔍 AI-Powered ATS Resume Analyzer

An intelligent **Resume vs Job Description Analyzer** built with **Google Gemini 2.0**, **Streamlit**, and **Python**. This tool helps job seekers analyze how well their resumes match a job description by simulating an Applicant Tracking System (ATS).

---

## ✨ Features

✅ Upload your resume (PDF)  
✅ Paste any job description (JD)  
✅ Get AI-based feedback on:

- Suitability summary and suggestions for improvement
- Relevant skills and experience
- Overall JD–Resume match score  
- Missing keywords or important mismatches  


---

## 📸 Demo

![📸 Demo](./Screenshot%20(37).png)
 


## 🧠 How It Works

- Parses PDF resumes using `PyPDF2`
- Accepts JD input from user
- Uses **Google Generative AI (Gemini-2.0)**
- Generates a structured response about match and improvement areas
- Displays it beautifully in **Streamlit**


## 🚀 Setup Instructions

### ✅ Prerequisites

- Python 3.8+
- Google Generative AI API Key  
  [Get it here](https://makersuite.google.com/app/apikey)

---

### ⚙️ Local Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/SNEHAVERMA22/MOD-ATS.git
cd mod-ats

#### 2. Create virtual environment
python -m venv venv
source venv/bin/activate       # On Linux/Mac
venv\Scripts\activate          # On Windows

#### 3. Install Dependencies
pip install -r requirements.txt

#### 4. Create .env File
GOOGLE_API_KEY=your-api-key-here

#### 5. Run the App
streamlit run app.py



