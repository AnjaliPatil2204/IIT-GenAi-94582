#Create a Streamlit application that takes a city name as input from the user.
#Fetch the current weather using a Weather API and use an LLM to explain the weather conditions in simple English.
import streamlit as st
import os
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
st.title("WeatherInfo")
city = st.text_input("Enter city name to get current weather explanation:")

if st.button("Get Weather"):
    if city.strip() == "":
        st.error("Please enter a valid city name.")
    else:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = os.popen(f'curl "{url}"').read()
        data = eval(response)
        if 'main' in data:
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            condition = data['weather'][0]['description']

            weather_info = f"The current temperature in {city} is {temperature} °C with a humidity of {humidity}%.The weather condition is described as {condition}."

            explanation_prompt = f"""
            You are a weather expert.

            Given the following weather information:
            {weather_info}

            Explain the weather conditions in simple English suitable for a general audience.
            """

            explanation = llm.invoke(explanation_prompt).content.strip()
            st.subheader("Weather Explanation")
            st.write(explanation)
        else:
            st.error("City not found. Please check the city name.")

        
    