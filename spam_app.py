import streamlit as st
import requests


st.title("Crunch some spam!")

URL_TEXT =  'https://spamfilterapi-kepp3lctya-uc.a.run.app/api/predict/text'
URL_FILE = 'https://spamfilterapi-kepp3lctya-uc.a.run.app/api/predict/file'

def display_output(r):
    prediction = 'spam!' if r.json()[0]['pred'] else 'ham.'
    spam_prob = r.json()[0]['spam_probability'] 
    ham_prob = 1 - spam_prob
    pred_prob = spam_prob if prediction=='spam!' else ham_prob
    st.write(f"## We think this email is {prediction} \n", f"Our model is {pred_prob*100:.2f}% confident in this classification.")

upload_type = st.selectbox('Choose your input type', ['.eml file upload', 'text entry'])

if upload_type == '.eml file upload':
    uploaded_file = st.file_uploader('Upload an email to classify!',['eml'])
    if uploaded_file:
        files = {'file':uploaded_file}
        r = requests.post(URL_FILE, files=files)
        display_output(r)

else:
    subject = st.text_input('Email subject')
    body = st.text_area('Email body')
    if subject or body:
        eml = {'instances':{'subject':[subject,],'body':[body,]}}
        r = requests.post(URL_TEXT,json = eml)
        display_output(r)


    