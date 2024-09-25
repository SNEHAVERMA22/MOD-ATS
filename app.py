import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(prompt,text,input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt,text,input])
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text



input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""



input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt4 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. As a Human Resource manager,
 assess the compatibility of the resume with the role. Give me what are the keywords that are missing
 Also, provide recommendations for enhancing the candidate's skills and identify which areas require further development in future.
"""


st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit1 = st.button("Detailed Analysis About the Resume")

submit3 = st.button("Percentage match")

submit4 = st.button("Keywords Missing in Resume")

if submit1:
    if uploaded_file is not None:
            text=input_pdf_text(uploaded_file)
            response=get_gemini_repsonse(input_prompt1,text,jd)
            st.subheader(response)
        
    else:
        st.write("Please uplaod the resume")
        
elif submit3:
    if uploaded_file is not None:
        if jd is not None:
            text=input_pdf_text(uploaded_file)
            response=get_gemini_repsonse(input_prompt3,text,jd)
            st.write(response)
        else:
            st.write("Please enter the job description to match")    
            
        
    else:
        st.write("Please uplaod the resume")
        
elif submit4:
    if uploaded_file is not None:
        if jd is not None:
            text=input_pdf_text(uploaded_file)
            response=get_gemini_repsonse(input_prompt4,text,jd)
            st.write(response)
            
        else:
            st.write("Please enter job description to find missing keywords")
            print("Please enter job description to find missing keywords")
        
    else:
        st.write("Please uplaod the resume")