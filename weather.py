import requests
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template

load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY not found. Please set it in the .env file.")

app = Flask(__name__)

def get_weather(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
        response = requests.get(url)
        response.raise_for_status()
        weather = response.json()
        return format_weather(weather)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            return "This city or country not Available."
        return f"Error fetching weather data: {e}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"

def format_weather(weather):
    try:
        location = weather["location"]["name"]
        country = weather["location"]["country"]
        temp_c = weather["current"]["temp_c"]
        condition = weather["current"]["condition"]["text"]
        return f"Weather in {location}, {country}: {temp_c}°C, {condition}"
    except KeyError:
        return "Location not found."

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_info = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_info = get_weather(city)
    return render_template('index.html', weather_info=weather_info)

if __name__ == "__main__":
    app.run(debug=True)