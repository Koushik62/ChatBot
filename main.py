import os
import discord
import requests
import json
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Initialize Discord client
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Constants



CHANNELS = ['your_channel_id']
WEATHER_API_KEY = os.getenv('WEATHER_KEY')
OPENAI_KEY = os.getenv('NEWOPENAI_API_KEY')

def get_coordinates(city_name):
    print(city_name)
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={WEATHER_API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    return data

# Function to fetch weather data from OpenWeatherMap API
def get_weather(city_name):
    data_1 = get_coordinates(city_name)
    lat = data_1[0]['lat']
    lon = data_1[0]['lon']
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}'
    response = requests.post(url)
    data = response.json()
    return data
    

# Event handler for when the bot is ready
@client.event
async def on_ready():
    print('The bot is online')

# Event handler for when a message is received
@client.event
async def on_message(message):
    print(message.content)
    if message.author.bot:
        return
    if str(message.channel.id) not in CHANNELS and client.user.id not in [user.id for user in message.mentions]:
        return
    # Check if the message is a weather command
    if 'weather' in message.content.lower():
    # If the message starts with '!weather'
        city_name = message.content.split('weather', 1)[1].strip()
        weather_data = get_weather(city_name)
        main_weather = weather_data['weather'][0]['main']
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        visibility = weather_data['visibility']
        wind = weather_data['wind']['speed']
        
      
       
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_KEY}",
                
            },
            data=json.dumps({
                "model": "openai/gpt-3.5-turbo", # Optional
                "messages": [
                    
                {"role": "user", "content":"The "
                                               f"weather detials of the {city_name}"
                                                f"main{main_weather}, temp:{temp}, humidity:{humidity}, visibility:{visibility}, windspeed:{wind}"
                                                "now give me content in such a very much intereactive way of messages using all these "
                                                "make the reponse as beatiful as possible and be sarcastic inlcude all emojis whatever is needed"
                                                "dont include any hastags, unneccesarily, and make sure that you bold  the main words, be funny and sarcastic, and make sure that is"
                                                "readable dont clutter all the content in one para, try to write 3-4 or more than that, but small paras, but dont give more than 10 lines"
                                                
                                               
                                                  
                                        
                    }
                ]
            })
            )
        content = response.json()['choices'][0]['message']['content']
       
        await message.channel.send(content)
       

    else:
       
       
       
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_KEY}",
                
            },
            data=json.dumps({
                "model": "openai/gpt-3.5-turbo", # Optional
                "messages": [
                    
                {"role": "user", "content":message}
                ]
            })
            )
        content = response.json()['choices'][0]['message']['content']
       
        await message.channel.send(content)
        
    # Write the updated chat history back to the file
   

    
# Run the bot
client.run(os.getenv('TOKEN'))
