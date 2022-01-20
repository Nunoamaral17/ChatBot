import re
from nltk import text
import requests
import json
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, commandhandler, dispatcher)
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
import TrainingBot as tb
from unidecode import unidecode


token = '1673860854:AAE2iGBByJU4nbipkdYIYWVzo59O16dfDzI' #Bot API Key Token
updater = Updater(token = token, use_context = True) 
api_key = "14e9af1a27d7b31769c3e5faa7e67633" #Open Weather Map API Key Token
    

def getweather(city):
        url = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&mode=json&units=metric&appid="+api_key
        response = requests.get(url)
        data = json.loads(response.text)
        return data

def userinput(update, context):
            #telegram user input
            inp = update.message.text
            inp2 = unidecode(inp)

            results = tb.model.predict([tb.bag_of_words(inp2, tb.words)])[0]
            results_index = tb.numpy.argmax(results)
            tag = tb.labels[results_index]
            
            #Se tiver 70% de confiança
            if results[results_index] > 0.7:
            
                for tg in tb.data["intents"]:
                    if tg["tag"] == tag:
                        responses = tg["responses"]
                context.bot.send_message(chat_id = update.effective_chat.id, text = tb.random.choice(responses))
            elif inp2[0:28] == "What is the weather like in ":
                weather(update,context)
                print("working")
            else:
                context.bot.send_message(chat_id = update.effective_chat.id, text = "Desculpe não percebo.")
            print(inp2[0:28])

def weather(update, context):
        #get user input
            aux2 = update.message.text
            weather = getweather(aux2[28:len(aux2)])
            aux = "The temperature in " + aux2[28:len(aux2)] +  " is " 
            temp = int(weather["main"]["temp"])
            temp = str(temp)
            context.bot.send_message(chat_id = update.effective_chat.id, text = str(aux + temp + "ºC"))

def welcome2(update, context):
    message = 'Ola' + ' ' + update.message.from_user.first_name 
    #print(message)
    context.bot.send_message(chat_id = update.effective_chat.id, text = message)

updater = Updater(token=token, use_context = True)

updater.dispatcher.add_handler(CommandHandler('bot', welcome2))
updater.dispatcher.add_handler(MessageHandler(Filters.text, userinput))
updater.dispatcher.add_handler(MessageHandler(Filters.text, userinput))

updater.start_polling()
print("RUNNING BOT")
updater.idle()