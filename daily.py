
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
import requests
import datetime
from time import sleep

api_key = '1061617283:AAFbmA0WAauyBHjhJn4E_g798eqCBBn2eXo'
group_chat_id = "-1001436792879"

bot = telegram.Bot(token=api_key)

def daily_check(context):
    status_success_count = 0
    url = 'http://18.140.255.180:8000'
    status = requests.get(url)
    if status.status_code == 200:
        status_success_count += 1
        print('1')
    url = 'https://18.140.255.180'
    status = requests.get(url, verify=False)
    if status.status_code == 200:
        status_success_count += 1
        print('2')
    url = 'http://18.140.255.180:8001/testpoint'
    status = requests.get(url)
    if status.status_code == 200:
        status_success_count += 1
        print('3')
    if status_success_count == 3:
            bot.send_message(chat_id=group_chat_id, text="Daily System Check\nAll Systems are up :)")
    
if __name__ == "__main__": 
    updater = Updater(api_key,use_context=True)
    dispatcher = updater.dispatcher
    job = updater.job_queue
    job_daily = job.run_daily(daily_check,time=datetime.time(2,0,0))
    updater.start_polling()
    updater.idle()
