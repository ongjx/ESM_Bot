
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
import requests
from datetime import datetime
from time import sleep

api_key = '1061617283:AAFbmA0WAauyBHjhJn4E_g798eqCBBn2eXo'
group_chat_id = "-1001436792879"

bot = telegram.Bot(token=api_key)

failure_count_cat = 0
failure_count_ticket = 0
failure_count_health = 0

def ping_system(context):
    time = datetime.now()
    date = time.strftime("%d/%m/%y")
    time = time.strftime("%X")
    cat_template = f"Hi @CTO @CTO Principal Assistant\nOn {date} at {time}, our team realised that ESMOS CAT System at http://18.140.255.180:8000 is down. We are currently investigating the cause and will update you as soon as possible."
    esmos_template = f"Hi @CTO @CTO Principal Assistant\nOn {date} at {time}, our team realised that ESMOS Ticketing System at https://18.140.255.180 is down. We are currently investigating the cause and will update you as soon as possible."
    heartbeat_template = f"Hi @CTO @CTO Principal Assistant\nOn {date} at {time}, our team realised that ESMOS Heartbeat at https://18.140.255.180 showed 'Server Dead'. We are currently investigating the cause and will update you as soon as possible."

    url = 'http://18.140.255.180:8000'
    status = requests.get(url)
    if status.status_code != 200:
        bot.send_message(chat_id=group_chat_id, text='CAT IS DOWN')
        bot.send_message(chat_id=group_chat_id, text=cat_template)
        global failure_count_cat
        failure_count_cat += 1
        if failure_count_cat == 5:
            try:
                context.job.schedule_removal()
            except:
                pass
    else:
        pass
        # bot.send_message(chat_id=group_chat_id, text="CAT SYSTEM is Up.")

    url = 'https://18.140.255.180'
    status = requests.get(url, verify=False)

    if status.status_code != 200:
        bot.send_message(chat_id=group_chat_id, text='ESMOS Ticketing IS DOWN!!!')
        bot.send_message(chat_id=group_chat_id, text=esmos_template)
        global failure_count_ticket
        failure_count_ticket += 1
        if failure_count_ticket == 5:
            try:
                context.job.schedule_removal()
            except:
                pass
    else:
        pass
        # bot.send_message(chat_id=group_chat_id, text="Ticketing System is up.")


    url = 'http://18.140.255.180:8001/testpoint'
    status = requests.get(url, )

    if status.text.strip() != '"Server Alive"':
        bot.send_message(chat_id=group_chat_id, text='ESMOS Heartbeat IS DEAD!!!')
        bot.send_message(chat_id=group_chat_id, text=heartbeat_template)
        global failure_count_health
        failure_count_health += 1
        if failure_count_health == 5:
            try:
                context.job.schedule_removal()
            except:
                pass
    else:
        pass
        # bot.send_message(chat_id=group_chat_id, text="ESMOS Heartbeat is Alive.")



if __name__ == "__main__": 
    updater = Updater(api_key,use_context=True)
    dispatcher = updater.dispatcher
    job = updater.job_queue
    job_min = job.run_repeating(ping_system,interval=60)
    updater.start_polling()
    updater.idle()
