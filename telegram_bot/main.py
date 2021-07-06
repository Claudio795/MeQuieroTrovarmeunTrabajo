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
from bot_utility import (
    start, get_job, location, update_info, cancel,
    JOB, LOCATION
    )


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
