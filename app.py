import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import re


load_dotenv()

# Use Streamlit secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def get_gemini_response(prompt,text,input):
    model=genai.GenerativeModel('gemini-2.0-flash-exp')
    response=model.generate_content([prompt,text,input])
    print(response)
    
    return response.text
    

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text



def extract_json_from_text(text):
    try:
        json_text = re.search(r"\{.*\}", text, re.DOTALL).group(0)
        return json.loads(json_text)
    except:
        return None

# Prompts
general_prompt = """
You are an experienced ATS evaluator and HR expert. Analyze the resume provided.
Give a general overview of strengths, weaknesses, and improvement tips without relying on any job description.
"""

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""



input_prompt3 = """
You are a skilled ATS scanner with a deep understanding of data science and ATS functionality.
Evaluate the resume against the provided job description and respond strictly in the following JSON format:

{
  "percentage_match": "85%",
  "missing_keywords": ["Python", "Kubernetes"],
  "final_thoughts": "Overall, the candidate has a solid background but lacks some key cloud skills."
}

DO NOT add any explanation outside the JSON.
"""

input_prompt4 = """
You are an skilled ATS (Applicant Tracking System) scanner with ATS functionality, 
your task is to evaluate the resume against the provided job description. As a Human Resource manager,
 Give me what are the keywords that are missing
 Also, provide recommendations for enhancing the candidate's skills and identify which areas require further development in future.
"""

# Streamlit UI
st.set_page_config(page_title="Smart ATS Resume Analyzer", page_icon="📄")
st.title("🧠 Smart ATS Resume Analyzer")
st.text("📄 Upload Resume for improving its ATS | 🧾 Optional Job Description for Precision Matching")
jd=st.text_area("Paste the Job Description(Optional)")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")






col1, col2, col3 = st.columns(3)
submit1 = col1.button("🧐 Detailed Analysis")
submit3 = col2.button("📊 % Match with JD")
submit4 = col3.button("🔍 Keywords Missing")

# Common resume extraction
if uploaded_file:
    resume_text = input_pdf_text(uploaded_file)

# Button 1: General or JD-based Evaluation
if submit1:
    if uploaded_file:
        if jd.strip():
            response = get_gemini_response(input_prompt1, resume_text, jd)
        else:
            response = get_gemini_response(general_prompt, resume_text, "")
        st.subheader("📝 Evaluation")
        st.write(response)
    else:
        st.warning("⚠️ Please upload a resume.")

elif submit3:
    if uploaded_file:
        if jd.strip():
            response = get_gemini_response(input_prompt3, resume_text, jd)
            data = extract_json_from_text(response)

            st.subheader("✅ Match Evaluation")
            if data:
                st.metric("🎯 Percentage Match", data.get("percentage_match", "N/A"))
                
                # Progress Bar
                match_str = data.get("percentage_match", "0%").replace("%", "").strip()
                if match_str.isdigit():
                    match_val = int(match_str)
                    st.progress(match_val)
                    
                    
                st.write("🚫 **Missing Keywords**")
                st.write(", ".join(data.get("missing_keywords", [])) or "None")

                st.write("💬 **Final Thoughts**")
                st.write(data.get("final_thoughts", "No thoughts provided."))
                
                # Download Button
                report_text = f"""
ATS Resume Analysis Report

Percentage Match: {data.get("percentage_match")}
Missing Keywords: {', '.join(data.get("missing_keywords", []))}
Final Thoughts: {data.get("final_thoughts")}
                """
                st.download_button("⬇️ Download ATS Report", data=report_text.strip(), file_name="ATS_Report.txt")
            else:
                st.warning("⚠️ Could not parse structured output. Showing raw text:")
                st.write(response)
        else:
            st.warning("⚠️ Please paste a job description to calculate match %.")  


# Button 3: Keywords Missing (JD mandatory)
elif submit4:
    if uploaded_file:
        if jd.strip():
            response = get_gemini_response(input_prompt4, resume_text, jd)
            st.subheader("🚫 Missing Keywords & Suggestions")
            st.write(response)
        else:
            st.warning("⚠️ Please paste a job description to identify missing keywords.")
    else:
        st.warning("⚠️ Please upload a resume.")
        
        

        
        
st.markdown("""
<hr style="margin-top: 3rem; margin-bottom: 1rem;border: 0.5px solid #ccc;">

<center>
    <small>
        Built with ❤️ by <strong>Sneha Verma</strong> <br>
        Final Year CSE @ IET Lucknow · GenAI | AI | ML Enthusiast <br>
        📧 <a href="mailto:sneha91493verma@gmail.com">sneha91493verma@gmail.com</a> |
        <a href="https://github.com/SNEHAVERMA22" target="_blank">GitHub</a> |
        <a href="https://www.linkedin.com/in/sneha-verma-42457025a/" target="_blank">LinkedIn</a>
    </small>
</center>
""", unsafe_allow_html=True)
