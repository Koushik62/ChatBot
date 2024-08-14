from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
import logging
import configparser

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def check_should_respond_or_not(userMessage):
  try:
    stream = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
          {
            "role": "system",
            "content": "You are a checker bot for checking the should be a response the user's message.You are designed to respond on a Discord channel.",
          },
          {
            "role": "user",
            "content": "Given a user's message and user's mention, your task is to check if there should be a response to user's message or not. Following is the creteria for checking: \n 1. The message says hello in some way. \n 2. The message says something about the bot or weather. \n 3. The userMessage is a question. \n OUTPUT_FORMAT: INI \n [response] \n is_related = True/False \n Say okay to continue.",
          },
          {
            "role": "assistant",
            "content": "Okay.",
          },
          {
            "role": "user",
            "content": f"userMessage: This bot is not good.",
          },
          {
            "role": "assistant",
            "content": "[response] \n should_respond = True",
          },  
          {
            "role": "user",
            "content": f"userMessage: How's the weather today ?",
          },
          {
            "role": "assistant",
            "content": "[response] \n should_respond = True",
          },
          {
            "role": "user",
            "content": f"userMessage: What's 4+7?",
          },
          {
            "role": "assistant",
            "content": "[response] \n should_respond = True",
          },
          {
            "role": "user",
            "content": f"userMessage: <@1227414582365212345> is bad guy",
          },
          {
            "role": "assistant",
            "content": "[response] \n should_respond = False",
          },
          {
            "role": "user",
            "content": f"userMessage: {userMessage}",
          },
        ])

    config = configparser.ConfigParser()
    config.read_string(stream.choices[0].message.content)
    should_respond = False
    for section in config.sections():
      should_respond = config[section]["should_respond"]
    return should_respond
  except Exception as e:
    logging.error(e)
    logging.error("token limit exceeded, Please change the open router api key")
    return False


def get_welcome_message(user_mention):
    try:
        stream = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a welcome message generator for a discord channel, in which the user gets weather updates given a city name.",
                },
                {
                    "role": "user",
                    "content": "Given a user's mention, your task is to generate a welcome message for them. The welcome message should contain a humorous tone. Tell the user to use the command '!weather <cityName>' to get weather details. \n Say okay to continue.",
                },
                {"role": "assistant", "content": "Okay."},
                {"role": "user", "content": "user: <@1227414582365261945>"},
                {
                    "role": "assistant",
                    "content": "🌟 Welcome, <@1227414582365261945>! Join for fun and quirky weather updates! Type `!weather <cityName>` to get weather details.😄🌦️",
                },
                {"role": "user", "content": f"user: {user_mention}"},
            ],
        )
        generated_text = stream.choices[0].message.content
    except Exception as e:
        logging.error(e)
        logging.error("token limit exceeded, Please change the open router api key")
        generated_text = (
            f"🌟 Welcome, {user_mention}! Join for fun and quirky weather updates! 😄🌦️"
        )

    return generated_text


def get_general_message(userMessage, userMention):
    try:
        stream = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a chatbot designed to respond in humurous and engaging way on a Discord channel dedicated to discussing weather in various cities. Users can ask for weather details by typing '!weather <cityName>'."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Given a user's message and user's mention. Generate relevant and humorous responses. Tell the user to use '!weather <cityName>' command to get the weather details. Also check if a user is talking about you or weather to another user by mentioning them in the message and give a funny and humurous response. Answer general questions and handle user mentions appropriately. Say okay to continue. \n Say okay to continue."
                    ),
                },
                {"role": "assistant", "content": "Okay."},
                {
                    "role": "user",
                    "content": f"userMention: <@1227414582365261945>, userMessage: Hello",
                },
                {
                    "role": "assistant",
                    "content": f"👋 Hey <@1227414582365261945>! Welcome to our weather channel! How can I assist you today? Interested in checking out the weather in a specific city? Just type !weather <cityName> and let's get started! 🌤️🌈",
                },
                {
                    "role": "user",
                    "content": f"userMention: <@1227414582365212345>, userMessage: What's 4+7 ?",
                },
                {
                    "role": "assistant",
                    "content": f"That would be 11! <@1227414582365212345>, If you've got any weather questions or need more math help, just let me know! 🌤️🧮",
                },
                {
                    "role": "user",
                    "content": f"userMention: <@1227414582365212345>, userMessage: This bot is not good <@1227235245225343>",
                },
                {
                    "role": "assistant",
                    "content": f"Hey <@1227414582365212345>, don't rush to reboot me just yet! Let's dial up another weather check—I'm here to be the sunshine on your cloudy day! 😄 <@1227235245225343>, Do you also think I am not good 🥹?",
                },
                {
                    "role": "user",
                    "content": f"userMention: <@1227414582365212345>, userMessage: How's the weather today ?, userMention: <@1227414582365212345>",
                },
                {
                    "role": "assistant",
                    "content": f"<@1227414582365212345> To give you today's weather, I'd need to know which city you're interested in! Could you specify the city for me? You remember the command right ? Offcourse you remember, its '!weather <cityName>' 🌍🌦",
                },
                {
                    "role": "user",
                    "content": f"userMention: {userMention}, userMessage: {userMessage}",
                },
            ],
        )
        generated_text = stream.choices[0].message.content
    except Exception as e:
        logging.error(e)
        logging.error("token limit exceeded, Please change the open router api key")
        generated_text = f"I didn't quite get that! 🤔 Could you try rephrasing your message? type !weather <cityName> to get the weather updates. 🌟"

    return generated_text


def get_weather_message(userMention, city, weatherDetails):
    sample_weather_details = "{'weather': [{'id': 721, 'main': 'Haze', 'description': 'haze', 'icon': '50n'}], 'main': {'temp': 29.03, 'feels_like': 32.79, 'temp_min': 29.03, 'temp_max': 29.03, 'pressure': 1009, 'humidity': 70}, 'visibility': 3000, 'wind': {'speed': 2.57, 'deg': 270}, 'clouds': {'all': 20}, 'dt': 1712848548,}"
    try:
        stream = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You're a humorous chatbot providing weather updates for a Discord channel.",
                },
                {
                    "role": "user",
                    "content": f"Given a user's mention, city name and weather details (in json format), your task is to generate a response to the user. The response should contain the weather details of the city in an interesting and humorous tone.  \n Say okay to continue.",
                },
                {"role": "assistant", "content": "Okay."},
                {
                    "role": "user",
                    "content": f"userMention: <@1227414582365212345>, city: Mumbai, weatherDetails: {sample_weather_details}",
                },
                {
                    "role": "assistant",
                    "content": "<@1227414582365212345>, let me whisk you through the whimsical weather in Mumbai! ** 🌅 \n \n - **Now**: 29°C but feels like 33°C. It's not just hot, it's *sneaky hot*. 😓 \n - **Sky**: Mostly Hazy. Like looking through a frosted glass. 🌫 \n - **Wind**: A gentle 2.57 m/s breeze, barely enough to flip a page. \n 🍃 - **Visibility**: Limited to 3 km. Perfect for hide-and-seek. \n 🕵️‍♂️ - **Humidity**: 70%. It's air with a side of water. \n \n 💧Stay cool or embrace the haze! Either way, it's a day to remember. 😂",
                },
                {
                    "role": "user",
                    "content": f"userMention: {userMention}, city: {city}, weatherDetails: {weatherDetails}",
                },
            ],
        )
        generated_text = stream.choices[0].message.content
        return generated_text
    except Exception as e:
        logging.error(e)
        logging.error("token limit exceeded, Please change the open router api key")
        generated_text = f"🌟 Hey {userMention}! Something seriously went wrong, Please try again! 🌤️🔍"
        return generated_text


def get_weather_wait_message(userMention, city):
    try:
        stream = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You're a humorous chatbot for a weather-focused Discord channel.",
                },
                {
                    "role": "user",
                    "content": f"Generate a brief one liner, humorous wait message for weather in mumbai. Mention user: <@1227414582365212345> and correct city name if city's name spelling is wrong. \n OUTPUT_FORMAT: INI \n [message] \n content = 'Wait message' \n correctedCityName = 'correct city name'",
                },
                {
                    "role": "assistant",
                    "content": "[message] \n content = **Fetching weather for Mumbai... ** <@1227414582365212345> ⏳ *In Mumbai, we use weather forecasts to predict the weather, not the lottery numbers! 😄*' \n correctedCityName = Mumbai",
                },
                {
                    "role": "user",
                    "content": f"userMention: <@1227414582365212345>, city: Jalndhar ",
                },
                {
                    "role": "assistant",
                    "content": "[message] \n content = **Hold tight** <@1227414582365212345> 🌤 *Jalandhar's forecast: Sunny with a chance of... wait, let’s make sure first! 🧐*' \n correctedCityName = Jalandhar",
                },
                {
                    "role": "user",
                    "content": f"userMention: {userMention}, city: {city}",
                },
            ],
        )
        generated_text = stream.choices[0].message.content

        config = configparser.ConfigParser()
        config.read_string(generated_text)
        for section in config.sections():
            content = config[section]["content"]
            correctedCityName = config[section]["correctedCityName"]

        return content, correctedCityName
    except Exception as e:
        logging.error(e)
        return (
            f"Please wait, {userMention}, fetching the forecast for {city}... 🌦️🤞",
            "",
        )
