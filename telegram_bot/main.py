from collections import UserList
import logging
import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    conversationhandler
)
from paho.mqtt.client import Client
from telegram.message import Message
from telegram.update import Update

from config import TOKEN

LOCATION = range(4)

# elenco funzioni del bot
def start(update, context):
    #all'interno di questa funzione instaureremo la connessione al broker
    
    reply_keyboard = [["/annulla"]]
    update.message.reply_text('Bot avviato, inviami la tua posizione per cominciare',
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True
        ),
    )
    return LOCATION

#funzione per richiedere un aggiornamento della posizione tramite comando 
def location(update, context):
    user = update.message.from_user["first_name"]
    user_location = update.message.location
    update.message.reply_text("Nuova posizione ricevuta")
    print(f"Coordinate di {user}: LAT: {user_location.latitude}, LONG: {user_location.longitude}")
    return ConversationHandler.END

# funzione per aggiornare la posizione
def update_location(update, context):
    user = update.message.from_user["first_name"]
    reply_keyboard = [["/annulla"]]
    update.message.reply_text(f'Ok {user}, inviami la tua nuova posizione',
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True
        ),
    )
    return LOCATION

# funzione per annullare un comando 
def cancel(update, context):
    #user = update.message.from_user
    update.message.reply_text("Operazione annullata.")
    return ConversationHandler.END


    


# funzione main ----------------------------------------
def main():
    upd = Updater(TOKEN, use_context=True)
    disp = upd.dispatcher

    #elenco di handler per i comandi del bot
    start_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states= {
            LOCATION: [MessageHandler(Filters.location, location)]
        },
        fallbacks=[CommandHandler("annulla", cancel)]
        )

    location_handler = ConversationHandler(
        entry_points=[CommandHandler("aggiorna_posizione", update_location)],
        states= {
            LOCATION: [MessageHandler(Filters.location, location)]
        },
        fallbacks=[CommandHandler("annulla", cancel)]
    )

    disp.add_handler(start_handler)
    disp.add_handler(location_handler)

    # avvio del bot, resta in esecuzione fino ad quando non
    #riceve un CTRL+C, SIGTERM O SIGABRT
    upd.start_polling()
    upd.idle()

if __name__ == "__main__":
    main()
