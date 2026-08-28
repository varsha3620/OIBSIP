import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:

        data = response.json()

        temperature = data["main"]["temp"]
        condition = data["weather"][0]["description"]

        return (
            f"The weather in {city} is {condition}. "
            f"The temperature is {temperature} degrees Celsius."
        )

    elif response.status_code == 404:

        return "Sorry, I could not find that location."

    else:

        print("Status code:", response.status_code)
        print("Response:", response.text)

        return "Sorry, I could not get the weather information."

