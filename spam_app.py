import streamlit as st
import requests


st.title("Crunch some spam!")

URL_TEXT =  'https://spamfilter.telcontar.info/api/predict/text'
URL_FILE = 'https://spamfilter.telcontar.info/api/predict/file'

def confidence_level(prob):
    if prob < .6:
        return "somewhat (<60%) confident in this classification"
    elif prob < .75:
        return "relatively (between 60% and 75%) confident in this classification"
    elif prob < .9:
        return "quite (between 75% and 90%) confident in this classification"
    else:
        return "very (>90%) confident in this classification"

def display_output(r):
    prediction = 'spam!' if r.json()[0]['pred'] else 'ham.'
    spam_prob = r.json()[0]['spam_probability'] 
    ham_prob = 1 - spam_prob
    pred_prob = spam_prob if prediction=='spam!' else ham_prob
    confidence = confidence_level(pred_prob)
    st.write(f"## We think this email is {prediction} \n", f"Our model is {confidence}.")

upload_type = st.selectbox('Choose your input type', ['text entry','.eml file upload'])

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

st.write("See more details at https://github.com/zcline91/spam_filter.")


    