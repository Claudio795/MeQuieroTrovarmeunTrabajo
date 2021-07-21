import json
from threading import Thread
from time import sleep


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

LOCATION, JOB, SENDVALUES, SENDLOC = range(4)

# -------------------------------------------- CLASSE BOT TELEGRAM ----------------------------------------------------------
class TelegramBot(object):
    def __init__(self, token, client, my_queues):
        self.token = token
        self.client = client
        self.queues = my_queues
        thread1 = Thread(target=self.run, args=())
        # thread1.daemon = True
        thread1.start()

    # Avvio -----------------------------------------------------------------------------------------------------------------
    def start(self, update, context):
        # messaggio di risposta dal bot
        update.message.reply_text('Bot avviato, che lavoro stai cercando?')
        return JOB

    # Comando per aggiungere il lavoro --------------------------------------------------------------------------------------
    def get_job(self, update, context):
        user = update.message.from_user
        job = update.message.text
        # salvo il lavoro scelto per passarlo alle funzioni successive
        context.user_data['qualification'] = job
        # print(f"{user.first_name} sta cercando un posto per {job}")

        update.message.reply_text(f'Grazie {user.first_name}, inviami ora la posizione in cui effettuare la ricerca')
        return LOCATION

    # comando per aggiungere la posizione dell'utente -----------------------------------------------------------------------
    def location(self, update, context):
        user = update.message.from_user
        user_location = update.message.location
        update.message.reply_text(
           "Nuova posizione ricevuta",
            reply_markup=ReplyKeyboardRemove())

        context.user_data['lat'] = user_location.latitude
        context.user_data['lon'] = user_location.longitude

        # print(f"Coordinate di {user.first_name}: LAT: {user_location.latitude}, LONG: {user_location.longitude}")
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

    # Comando per l'invio dei valori ----------------------------------------------------------------------------------------
    def send(self, update, context):

        payload = context.user_data
        str_payload = json.dumps(payload)
        # print(str_payload)
        self.client.publish(topic="user/info", payload=str_payload)

        update.message.reply_text(
            "I tuoi dati sono stati inviati.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END


    # Comando per aggiornare posizione e lavoro -------------------------------------------------------------------------------
    def update_info(self, update, context):
        user = update.message.from_user
        reply_keyboard = [["/annulla"]]
        update.message.reply_text(f'Ok {user.first_name}, inviami il nuovo lavoro richiesto',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
            ),
        )
        return JOB

    # Comando per annullare -------------------------------------------------------------------------------------------------- 
    def cancel(self, update, context):
        update.message.reply_text("Operazione annullata.",
        reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    # Comando per visualizzare i link dei lavori disponibili -----------------------------------------------------------------

    def job_message(self, update, context):
        job_queue = self.queues['node/jobs']
        payload = job_queue.get()
        if len(payload) > 4096:
            list_payload = payload.split("\n\n")
            for x in range(0, len(list_payload), 5):
                str_payload = '\n\n'.join([str(item) for item in list_payload[x:x+5]])
                update.message.reply_text(str_payload)
        else:
            update.message.reply_text(payload)

    # Comando per visualizzare il meteo locale -------------------------------------------------------------------------------
    def weather(self, update, context):
        reply_keyboard = [["/annulla"]]
        update.message.reply_text('Mandami la posizione interessata',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
            ),
        )
        return SENDLOC

    def send_location(self, update, context):
        user_location = update.message.location

        context.user_data['lat'] = user_location.latitude
        context.user_data['lon'] = user_location.longitude

        pub_payload = context.user_data
        str_payload = json.dumps(pub_payload)

        self.client.publish(topic="user/position", payload=str_payload)

        update.message.reply_text('Posizione inviata, ti invio il meteo locale:',
        reply_markup=ReplyKeyboardRemove())

        sleep(2)
        weather_queue = self.queues['node/weather']
        rec_payload = weather_queue.get()

        update.message.reply_text(rec_payload)

        #return RECWEATHER
        return ConversationHandler.END

    # Comando per visualizzare le news ogni mattina --------------------------------------------------------------------------

    def news_message(self, update, context):
        news_queue = self.queues['node/news']
        payload = news_queue.get()
        

        # TODO: modificare a seconda del messaggio che ricevo
        if len(payload) > 4096:
            list_payload = payload.split("\n\n")
            for x in range(0, len(list_payload), 5):
                str_payload = '\n\n'.join([str(item) for item in list_payload[x:x+5]])
                update.message.reply_text(str_payload)
        else:
            update.message.reply_text(payload)


    # run -------------------------------------------------------------------------------------------------------------------
    def run(self):
        self.upd = Updater(self.token, use_context=True)
        self.disp = self.upd.dispatcher

        #elenco di handler per i comandi del bot
        start_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states= {
                LOCATION: [MessageHandler(Filters.location, self.location)],
                JOB: [MessageHandler(Filters.text, self.get_job)],
                SENDVALUES: [MessageHandler(Filters.text & ~Filters.command, self.send)]
            },
            fallbacks=[CommandHandler("annulla", self.cancel)]
            )

        update_handler = ConversationHandler(
            entry_points=[CommandHandler("aggiorna_informazioni", self.update_info)],
            states= {
                LOCATION: [
                    MessageHandler(Filters.location, self.location),
                    CommandHandler("annulla", self.cancel)
                    ],
                JOB: [
                    MessageHandler(Filters.text & ~Filters.command, self.get_job),
                    # CommandHandler("annulla", cancel)
                    ],
                SENDVALUES: [MessageHandler(Filters.text & ~Filters.command, self.send)]
            },
            fallbacks=[CommandHandler("annulla", self.cancel)]
        )

        # weather_handler = CommandHandler("meteo", self.weather_message)
        weather_handler = ConversationHandler(
            entry_points=[CommandHandler("meteo", self.weather)], 
            states= {
                SENDLOC: [
                    MessageHandler(Filters.location, self.send_location),
                    CommandHandler("annulla", self.cancel)
                ]
            },
            fallbacks=[CommandHandler("annulla", self.cancel)]
        )

        job_handler = CommandHandler("lavori", self.job_message)
        news_handler = CommandHandler("news", self.news_message)

        self.disp.add_handler(start_handler)
        self.disp.add_handler(update_handler)

        self.disp.add_handler(job_handler)
        self.disp.add_handler(weather_handler)
        self.disp.add_handler(news_handler)

        
        # job_queue = self.upd.job_queue
        #job_daily = job_queue.run_daily(self.news_message, days=(0, 1, 2, 3, 4, 5, 6), time=time(hour=9, minute=00, second=00))
        # job_queue.run_once(self.news_message, 15)

        # avvio del bot, resta in esecuzione fino ad quando non
        #riceve un CTRL+C, SIGTERM O SIGABRT
        self.upd.start_polling()