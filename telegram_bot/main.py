import logging
import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
)
from paho.mqtt.client import Client

from telegram.ext.callbackcontext import CallbackContext
from telegram.message import Message
from telegram.update import Update

from config import TOKEN


# elenco funzioni del bot
def start(update, context):
    #all'interno di questa funzione instaureremo la connessione al broker
    msg = (
        "Bot avviato"
    )
    update.message.reply_text(msg)

# Test_1: ritorno della posizione GPS
def get_location(update, context):
    print("messaggio ricevuto")
    print(update.message.from_user)
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message

    lat = message.location.latitude
    lng = message.location.longitude
    #update.message.reply_text(f"latitudine: {lat}, longitudine: {lng}")
    print(f"latitudine: {lat}, longitudine: {lng}")
    


# ----------------------------------------
def main():
    upd = Updater(TOKEN, use_context=True)
    disp = upd.dispatcher

    disp.add_handler(CommandHandler("start", start))

    disp.add_handler(MessageHandler(Filters.location, get_location))

    upd.start_polling()
    upd.idle()

if __name__ == "__main__":
    main()
