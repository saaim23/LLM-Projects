import google.generativeai as gen
import base64
import io
import pdf2image
from PIL import Image
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

gen.configure(api_key=os.getenv('API_KEY'))


def get_gemini_response(input, pdf_content, prompt):
    model = gen.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        img_bytes_arr = io.BytesIO()
        first_page.save(img_bytes_arr, format='JPEG')
        img_bytes_arr = img_bytes_arr.getvalue()

        pdf_parts = [
            {
                'mime_type': 'image/jpeg',
                'data': base64.b64encode(img_bytes_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError('No file uploaded')


st.set_page_config(page_title='ATS Resume')
st.header('ATS(Applicant Tracking System)')
input_text = st.text_area(
    'Job', placeholder="Write your job description here", key='input')
uploaded_file = st.file_uploader('Upload', type=['pdf'])

if uploaded_file is not None:
    st.write('pdf')

submit1 = st.button('Tell Me About the Resume')
submit2 = st.button('How can i Imporve my Skills')
submit3 = st.button('Percentage Match')

input_prompt1 = """
As an experienced HR professional with  expertise across various career fields, 
your task is to review the provided resume in comparison to the job description for those profiles.
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job role."""

input_prompt2 = """
Your are experienced in every field, you would like to know how the provided resume can be tailored to better match the job description for these profiles.
"""
input_prompt_3 = """
"You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of every field and extensive knowledge of ATS functionality.
 Your task is to evaluate the resume against the provided job description and provide the percentage of match.
 First, the output should be presented as a percentage, 
 followed by the missing keywords, and finally, share your overall thoughts on the match."""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader('The')
        st.write(response)
    else:
        st.write('Please Uplaod')
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("Response ")
        st.write(response)
    else:
        st.write('Please Upload')
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt_3, pdf_content, input_text)
        st.subheader("Response ")
        st.write(response)
    else:
        st.write('Please Uplaod')
