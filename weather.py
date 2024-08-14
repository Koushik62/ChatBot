import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

def get_weather(city):
    try:
        weather_api_key = os.getenv('WEATHER_API_KEY')
    
        # Fetch latitude and longitude of the city
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={weather_api_key}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if geo_response.status_code == 200:
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']
            
            # Fetch weather details using latitude and longitude
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()
        
            if weather_response.status_code == 200:
                return weather_data
                # weather_description = weather_data["weather"][0]["description"]
                # temperature = weather_data["main"]["temp"]
                # return f"The weather in {city} is {weather_description} with a temperature of {temperature}°C."
            else:
                logging.error(weather_response.text)
                return "Error fetching weather information"
        else:
            logging.error(geo_response.text)
            return "Error fetching city information"
    except Exception as e:
        logging.error(e)
        return "Error fetching weather information"
