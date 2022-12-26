from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import openai
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()


# Set the value of token using the TOKEN environment variable
token = os.environ['TOKEN']

# Set the value of openai.api_key using the OPENAI_API_KEY environment variable
openai.api_key = os.environ['OPENAI_API_KEY']

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Ask Me Anything :)")
    
def help(update: Update, context: CallbackContext):
    update.message.reply_text("Ask anything to the bot ;) \n 1. Ask any question in chat \n 2. Use \img to generate a image")

def img(update: Update, context: CallbackContext):
    img = update['message']['text'].split('/img ')[1]
    response = openai.Image.create(
                  prompt=img,
                  n=1,
                  size="1024x1024"
                )
    url = response['data'][0]['url']
    update.message.reply_text(url)

def do_something(user_input):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=user_input,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text

def reply(update: Update, context: CallbackContext):
    user_input = update.message.text
    res = do_something(user_input)
    #print(user_input)
    #print(res)
    update.message.reply_text(res)

updater = Updater(token, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('help', help))
dp.add_handler(CommandHandler('img', img))
dp.add_handler(MessageHandler(Filters.text, reply))
updater.start_polling()
updater.idle()