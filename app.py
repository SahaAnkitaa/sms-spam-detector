
import string
import os

import nltk
#nltk.download('punkt')
#nltk.download('stopwords')

import streamlit as st
import pickle

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

# Set the NLTK data path to the local nltk_data folder
nltk.data.path.append(os.path.join(os.getcwd(), 'nltk_data'))

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf= pickle.load(open('vectorizer.pkl', 'rb'))
model= pickle.load(open('model.pkl', 'rb'))

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #360135; /* Dark purple background */
        opacity: 0.9;
    }
    .stTextInput>div>div>div>div>input {
        background-color: #f0f0f0; /* Light grey background */
        color: #333333; /* Dark grey text color */
        border-radius: 10px; /* Rounded corners */
    }
    .stButton>button {
        background-color: #b320b0; /* Green background */
        color: white; /* White text color */
        border-radius: 10px; /* Rounded corners */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('SMS Spam Detector')

input_sms= st.text_input("Enter your message")

transformed_sms= transform_text(input_sms)

vector_input = tfidf.transform([transformed_sms])

if st.button('Predict'):
    res= model.predict(vector_input)[0]

    if res==1:
        st.header("Spam")
    else:
        st.header("Not Spam")

