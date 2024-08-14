import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv
import os
import openRouter
import weather

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CustomLogger")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info('Bot is ready.')
    
@bot.event
async def on_member_join(member):
    logger.info(f'{member} has joined the server.')
    channel = member.guild.system_channel
    if channel:
        welcomeMessage = openRouter.get_welcome_message(member.mention)
        await channel.send(welcomeMessage)

# Event to respond to messages
@bot.event
async def on_message(message):
    
    if not message.content:
        return
    
    # Check if the message is from the bot itself to avoid infinite loops
    if message.author == bot.user:
        return
    
    
    # # Fetch the last 5 messages from the same author
    # last_messages = await message.channel.history(limit=100)
    # logger.info(f'last_messages: {last_messages}')
    # last_five_messages = [msg for msg in last_messages if msg.author == message.author][:5]

    # # Log or process these messages
    # for msg in last_five_messages:
    #     print(msg.content)
    
    if message.content.lower().startswith('!weather'):
        try:
            city = message.content.split(' ')[1]
            async with message.channel.typing():
                wait_message, correctedCityName = openRouter.get_weather_wait_message(message.author.mention, city)
            await message.channel.send(wait_message)
        except:
            await message.channel.send(f"{message.author.mention} Please provide a city name (e.g. !weather Mumbai)")
            return
        async with message.channel.typing():
            weather_data = weather.get_weather(correctedCityName)
            filtered_weather_data = weather_data
            if weather_data and isinstance(weather_data, dict):
                keys_to_keep = {'weather', 'main', 'wind', 'clouds', 'visibility'}
                filtered_weather_data = {k: v for k, v in weather_data.items() if k in keys_to_keep}
            weather_message = openRouter.get_weather_message(message.author.mention, correctedCityName, filtered_weather_data)
        await message.channel.send(weather_message)
        return

    # check if the bot is mentioned
    if bot.user.mentioned_in(message):
        async with message.channel.typing():
            general_message = openRouter.get_general_message(message.content, message.author.mention)
        await message.channel.send(general_message)
        return
    
    should_respond = openRouter.check_should_respond_or_not(message.content)
    should_respond_anyhow = True if 'bot' in message.content.lower() or 'weather' in message.content.lower() else False
    is_someone_mentioned = True if message.mentions.__len__() > 0 else False
    if (should_respond == 'True' and (not is_someone_mentioned)) or should_respond_anyhow == True:
        async with message.channel.typing():
            general_message = openRouter.get_general_message(message.content, message.author.mention)
        await message.channel.send(general_message)
        return
    
# Run the bot with its token
bot.run(os.getenv('DISCORD_TOKEN'))