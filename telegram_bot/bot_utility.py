from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)

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
    update.message.reply_text("Operazione annullata.",
    reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


    