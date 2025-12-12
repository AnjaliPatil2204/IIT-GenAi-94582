import requests

api_key = "722da81f13354bc4090cf95b4273e953"

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    return response  # return the full response so main.py can decide
