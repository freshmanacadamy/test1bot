from flask import Flask, request
import telebot
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ----- Example bot handlers -----
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Bot is active on Vercel 🚀")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, f"You said: {message.text}")

# ----- Webhook route -----
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# ----- Simple home page -----
@app.route('/')
def index():
    return "Bot is running! ✅"

# ----- Run locally (for testing only) -----
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://<YOUR_VERCEL_URL>/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))