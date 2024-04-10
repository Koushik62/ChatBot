import discord
import requests
from openai import OpenAI

# Replace with your OpenWeatherMap API Key
api_key = "d13a259cfcb7e89a51a23f761b3a9924npm install openai@^4.0.0"

# Replace with your OpenRouter.ai API Key
openai.api_key = "YOUR_OPENROUTER_AI_API_KEY"

# Discord Bot Setup
client = discord.Client()

# Function to fetch weather data
def get_weather(city):
  url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
  response = requests.get(url)
  return response.json()

# Function to generate creative response with ChatGPT
def generate_creative_response(prompt):
  response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      max_tokens=100,
      n=1,
      stop=None,
      temperature=0.7,
  )
  return response.choices[0].text.strip()

# Function to handle weather commands
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith("!weather"):
    city = message.content.split()[1]

    try:
      weather_data = get_weather(city)
      temp = weather_data["main"]["temp"]
      desc = weather_data["weather"][0]["description"]

      # Basic weather response with a touch of personality
      response = f"The weather in {city} is currently {temp:.1f}°C and {desc}. Don't forget to pack an umbrella... unless you're a mermaid "

      # Generate a creative response using ChatGPT (optional)
      creative_prompt = f"Write a haiku poem about the weather in {city} based on the description '{desc}'"
      creative_response = generate_creative_response(creative_prompt)
      response += f"\n\n{creative_response}"

      await message.channel.send(response)
    except Exception as e:
      # Handle errors with humor
      await message.channel.send(f"Oops! Seems like I have a case of temporary amnesia. I can't find weather data for '{city}' right now. Maybe it's hiding from the rain clouds? Try again later!")

# Run the bot
client.run("YOUR_BOT_TOKEN")
