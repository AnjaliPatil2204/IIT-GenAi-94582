#Show Login Form. If login is successful (fake auth if username & passwd is same, 
#consider valid user), show weather page. There input a city name
#from text box and display current weather information. Provide a logout
#button and on its click, display thanks message.
import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")
st.title("Weather App")
st.subheader("Login to access weather information")
# Login Form
with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")
    if submitted:
        if username == password and username != "":
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success("Login successful!")
        else:
            st.error("Invalid credentials. Please try again.")

if 'logged_in' in st.session_state and st.session_state['logged_in']:
    st.subheader(f"Welcome, {st.session_state['username']}!")
    city = st.text_input("Enter city name to get current weather:")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    if st.button("Get Weather") and city:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            st.write(f"**Temperature:** {data['main']['temp']} °C")
            st.write(f"**Humidity:** {data['main']['humidity']} %")
            st.write(f"**Condition:** {data['weather'][0]['description']}")
        else:
            st.error("City not found. Please check the city name.")

    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state.pop('username', None)
        st.success("You have been logged out.")

