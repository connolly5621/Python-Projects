from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load API key from .env
load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')

# Route for homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        units = request.form['units']
        weather_data = get_weather(city, units)
    return render_template('index.html', weather=weather_data)


def get_weather(city, units):
    unit_symbol = '°C' if units == 'metric' else '°F'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}'
    response = requests.get(url)


    if response.status_code == 200:
        data = response.json()
        weather = {
            'city': city,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'icon': data['weather'][0]['icon'],
            'unit_symbol': unit_symbol
        }
        return weather
    else:
        return None
    

if __name__ == '__main__':
    app.run(debug=True)