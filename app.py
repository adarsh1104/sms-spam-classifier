import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
from win32com.client import Dispatch

ps = PorterStemmer()

def speak(Text):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.speak(Text)

def transform_Text(Text):
    Text = Text.lower()
    Text = nltk.word_tokenize(Text)

    y = []
    for i in Text:
        if i.isalnum():
           y.append(i)

    Text = y[:]
    y.clear()

    for i in Text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    Text = y[:]
    y.clear()

    for i in Text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title("Spam/ham Detection")

input_sms = st.text_area("Enter the message")

if st.button('Predict'):


    transformed_sms = transform_Text(input_sms)

    vector_input = tfidf.transform([transformed_sms])

    result = model.predict(vector_input)[0]

    if result == 1:
        st.header("This is a spam mail")
        speak("This is a spam mail")
    else:
        st.header("This is not a spam mail")
        speak("This is not a spam mail")