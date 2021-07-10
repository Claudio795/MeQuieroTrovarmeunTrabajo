import json
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

LOCATION, JOB, SENDVALUES = range(3)

# COMANDI DEL BOT ------------------------------------------------------------------------------------------------------

# Avvio -----------------------------------------------------------------------------------------------------------------
def start(update, context):
    # messaggio di risposta dal bot
    update.message.reply_text('Bot avviato, che lavoro stai cercando?')
    return JOB

# Comando per aggiungere il lavoro --------------------------------------------------------------------------------------
def get_job(update, context):
    user = update.message.from_user
    job = update.message.text
    # salvo il lavoro scelto per passarlo alle funzioni successive
    context.user_data['qualification'] = job
    print(f"{user.first_name} sta cercando un posto per {job}")

    update.message.reply_text(f'Grazie {user.first_name}, inviami ora la posizione in cui effettuare la ricerca')
    return LOCATION

# comando per aggiungere la posizione dell'utente -------------------------------------------------------------------------
def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    update.message.reply_text(
        "Nuova posizione ricevuta",
        reply_markup=ReplyKeyboardRemove())

    # inserisco le coordinate nella queue
    context.user_data['lat'] = user_location.latitude
    context.user_data['lon'] = user_location.longitude

    print(f"Coordinate di {user.first_name}: LAT: {user_location.latitude}, LONG: {user_location.longitude}")
    reply_keyboard = [
                        ["Si"],
                        ["/annulla"]
                        ]

    update.message.reply_text(
        "Dati ricevuti, inviare?",
        reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True
        ),
    )

    return SENDVALUES

# Comando per l'invio dei valori ---------------------------------------------------------------------------------------
def send(update, context):

    payload = context.user_data
    str_payload = json.dumps(payload)
    print(str_payload)      # test
    client.publish(topic="user/info", payload=str_payload)

    update.message.reply_text(
        "I tuoi dati sono stati inviati.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


# Comando per aggiornare posizione e lavoro -------------------------------------------------------------------------------
def update_info(update, context):
    user = update.message.from_user
    reply_keyboard = [["/annulla"]]
    update.message.reply_text(f'Ok {user.first_name}, inviami il nuovo lavoro richiesto',
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True
        ),
    )
    return JOB

# Comando per annullare -------------------------------------------------------------------------------------------------- 
def cancel(update, context):
    update.message.reply_text("Operazione annullata.",
    reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
  