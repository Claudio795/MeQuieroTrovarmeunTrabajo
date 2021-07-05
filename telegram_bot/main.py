import logging
import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)
from paho.mqtt.client import Client
from telegram.message import Message
from telegram.update import Update

from config import TOKEN

LOCATION, JOB = range(2)

# elenco funzioni del bot
def start(update, context):
    #all'interno di questa funzione instaureremo la connessione al broker
    
    update.message.reply_text('Bot avviato, che lavoro stai cercando?')
    return JOB

# funzione per aggiungere il lavoro per cui ricevere aggiornamenti
def get_job(update, context):
    user = update.message.from_user["first_name"]
    job = update.message.text
    print(f"{user} sta cercando un posto per {job}")
    update.message.reply_text(f'Grazie {user}, inviami ora la posizione in cui effettuare la ricerca')
    return LOCATION

# funzione per richiedere un aggiornamento della posizione tramite comando 
def location(update, context):
    user = update.message.from_user["first_name"]
    user_location = update.message.location
    update.message.reply_text(
        "Nuova posizione ricevuta",
        reply_markup=ReplyKeyboardRemove())

    print(f"Coordinate di {user}: LAT: {user_location.latitude}, LONG: {user_location.longitude}")
    return ConversationHandler.END

# funzione per aggiornare posizione è lavoro
def update_info(update, context):
    user = update.message.from_user["first_name"]
    reply_keyboard = [["/annulla"]]
    update.message.reply_text(f'Ok {user}, inviami il nuovo lavoro richiesto',
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True
        ),
    )
    return JOB

# funzione per annullare un comando 
def cancel(update, context):
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
            LOCATION: [MessageHandler(Filters.location, location)],
            JOB: [MessageHandler(Filters.text, get_job)]
        },
        fallbacks=[CommandHandler("annulla", cancel)]
        )

    update_handler = ConversationHandler(
        entry_points=[CommandHandler("aggiorna_informazioni", update_info)],
        states= {
            LOCATION: [
                MessageHandler(Filters.location, location),
                CommandHandler("annulla", cancel)
                ],
            JOB: [
                MessageHandler(Filters.text & ~Filters.command, get_job),
                # CommandHandler("annulla", cancel)
                ]
        },
        fallbacks=[CommandHandler("annulla", cancel)]
    )

    disp.add_handler(start_handler)
    disp.add_handler(update_handler)

    # avvio del bot, resta in esecuzione fino ad quando non
    #riceve un CTRL+C, SIGTERM O SIGABRT
    upd.start_polling()
    upd.idle()

if __name__ == "__main__":
    main()
