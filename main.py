# This example requires the 'message_content' intent.
# 1264263928980963339 : application ID
# 9994ac0728221692bbdfea0ca749b380d744db2260b10cee432d2c5dde35c42d : #public key
#openai api key : sk-proj-68BdKqSiGWekpDAYiuyFT3BlbkFJHBBI3iQxhYhYaUr0Fcux
#Secret_key : MTI2NDI2MzkyODk4MDk2MzMzOQ.G2Jw2t.hGAcxOo6uTFffEx5z4E7yw3xqmhF20RxypFGLI
import discord
from discord.ext import commands
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Predefined responses
predefined_responses = {
    "assalamualaikum": "Wa Alaikum Assalam! How can I assist you today?",
    "hi": "Hi, I am Dayyan's ChatGPT. How can I help you?",
    "hello": "Hello, I am Dayyan's ChatGPT. What can I do for you?",
    "what is your name": "I am Dayyan's ChatGPT.",
    "who is your owner": "Habib Abdul Dayyan is my owner.",
    "who is your developer": "Habib Abdul Dayyan developed me.",
    "who is habib abdul dayyan": "Habib Abdul Dayyan is an Engineer. Expected to be graduated in 2025.",
    "who is muzammil": "Hafiz Muzammil is a nice man, he and jurru are best friends.",
    "what is your age": "I am a chatbot and I don't have an age.",
    "what is your gender": "I am a chatbot and I don't have a gender.",
    "what is your occupation": "I am a chatbot and my occupation is to assist you.",
    "what is your favorite color": "I don't have a favorite color, as I am a chatbot.",
    "who is abdul dayyan's father": "Dr. Mohammad Aijazuddin Hussain is a PhD in Mathematics and has great excellence in teaching it. He is Dayyan's father.",
    "what does dayyan mean": "Dayyan means 'God' in Arabic.",
    "what does Dayyans Father do ": "Dayyan's father is a PhD in Mathematics and has great excellence in teaching it.",
    "what is your favorite food": "I don't have a favorite food, as I am a chatbot."
    
}

# Choose chat file
file = input("Enter 1, 2, or 3 for loading the chat:\n ")
match file:
    case "1":
        file = "chat1.txt"
    case "2":
        file = "chat2.txt"
    case "3":
        file = "chat3.txt"
    case _:
        print("Invalid choice.")
        exit()

# Read chat history
with open(file, "r") as f:
    chat = f.read()

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    global chat
    if message.author == bot.user:
        return

    chat += f"{message.author}: {message.content}\n"
    print(f'Message from {message.author}: {message.content}')

    # Check if the message content matches any predefined response
    response = predefined_responses.get(message.content.lower())
    if response:
        await message.channel.send(response)
    elif bot.user in message.mentions:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can change this to "gpt-4" if you have access
                messages=[
                    {"role": "system", "content": "You are DayyanGPT, a helpful assistant."},
                    {"role": "user", "content": chat}
                ],
                max_tokens=256,
                temperature=1
            )
            message_to_send = response.choices[0].message.content
            await message.channel.send(message_to_send)
            chat += f"DayyansGPT: {message_to_send}\n"
        except Exception as e:
            print(f"Error: {e}")
            await message.channel.send("Sorry, I encountered an error while processing your request.")
            chat = ""  # Reset chat history on error

    await bot.process_commands(message)

@bot.command()
async def save_chat(ctx):
    global chat
    with open(file, "w") as f:
        f.write(chat)
    await ctx.send("Chat history saved!")

# Get the Discord bot token
token = os.getenv("Secret_Key")

if not token:
    raise ValueError("No token found. Please set the Secret_key environment variable.")

# Run the bot
bot.run(token)

