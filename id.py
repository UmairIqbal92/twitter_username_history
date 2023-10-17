import tweepy
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Command
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
import time

# Set up Twitter API keys and access tokens
consumer_key = "OBm5bSC8uz0nOBH5Q75gYOyQc"
consumer_secret = "8WSTF2Jgsmb7DwjjKC70hDpHljSWepcAjRC7h9NlFRbfxI6dSY"
access_token = "1245060649832546304-GoqUbYSGxd9RUS5yYiAn5S0heNJUK2"
access_token_secret = "60eMFn12a9tFEBVVI8Fb8xZB72iYqenelc7OQqHKQi9mE"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Initialize the bot and dispatcher
bot = Bot(token="5841151417:AAE0wEHvTpoic_DEJnQpqlHTRgOXsJPsLHw")  # Replace with your actual bot token
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Load existing username history from a file
username_history = []

try:
    with open("username_history.txt", "r") as history_file:
        for line in history_file:
            username, timestamp = line.strip().split(" - ")
            username_history.append((username, timestamp))
except FileNotFoundError:
    pass

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Welcome to the Twitter Username Tracker Bot! Send /check_username to get started.")

@dp.message_handler(commands=['check_username'])
async def check_username_command(message: types.Message):
    await message.answer("Please enter the Twitter username you want to track.")

@dp.message_handler(lambda message: message.text and not message.text.startswith('/'))
async def username_checking(message: types.Message):
    username = message.text.strip()
    try:
        user = api.get_user(screen_name=username)

        current_username = user.screen_name
        creation_time = user.created_at.strftime("%Y-%m-%d %H:%M:%S")

        username_history.append((current_username, creation_time))

        # Sort the username_history list by the creation date in ascending order
        username_history.sort(key=lambda x: x[1])

        # Save the updated username history to the file
        with open("username_history.txt", "w") as history_file:
            for entry in username_history:
                history_file.write(f"{entry[0]} - {entry[1]}\n")

        history_message = "\n".join([f"{username} - {timestamp}" for username, timestamp in username_history])

        reply_text = f"Twitter username change history (ascending order by date):\n{history_message}"

        await message.answer(reply_text, parse_mode=ParseMode.MARKDOWN)
    except tweepy.TweepError as e:
        await message.answer(f"Error: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
