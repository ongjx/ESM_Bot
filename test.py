import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
import requests
from datetime import datetime
from time import sleep

api_key = '1061617283:AAFbmA0WAauyBHjhJn4E_g798eqCBBn2eXo'
group_chat_id = "363882054"

bot = telegram.Bot(token=api_key)
updater = Updater(api_key,use_context=True)
dispatcher = updater.dispatcher


def start(update,context):
    bot.send_message(chatid= group_chat_id, text='Type /ping to begin pinging ESMOS and CAT')


def ping(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    # context.job
    # print('here',update.message.text)
    # ping_system(update)


def ping_system():

    url = 'http://18.140.255.180:8000'
    status = requests.get(url)
    if status.status_code != 200:
        bot.send_message(chat_id=group_chat_id, text='CAT IS DOWN')
    else:
        bot.send_message(chat_id=group_chat_id, text='CAT IS UP')

    url = 'https://18.140.255.180'
    if status.status_code != 200:
        bot.send_message(chat_id=group_chat_id, text='ESMOS IS DOWN')
    else:
        bot.send_message(chat_id=group_chat_id, text='ESMOS IS UP')
        
    sleep(5)

# def ping_min(context):
#     context.bot.send


def stop(update,context):
    update.send_message(chat_id=group_chat_id, text='Stopping the bot')
    update.stop()



start_handler = CommandHandler('start',start)
stop_handler = CommandHandler('stop',stop)
job_handler = Job(ping_system, 60,True)

ping_handler = MessageHandler(Filters.text, ping)
ping_sys_handler = MessageHandler(Filters.text, ping_system)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(ping_handler)
dispatcher.add_handler(ping_sys_handler)

updater.start_polling()
updater.idle()
