import json
from threading import Thread
from queue import Queue

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)
import paho.mqtt.client as mqtt
from paho.mqtt.client import Client

from config import TOKEN, USERNAME, PASSWORD

LOCATION, JOB, SENDVALUES = range(3)

# -------------------------------------------- CLASSE CLIENT MQTT ----------------------------------------------------------
class MQTTClient(object):
    def __init__(self, username, password, my_queue):
        self.username = username
        self.password = password
        self.queue = my_queue
        thread0 = Thread(target=self.run, args=())
        thread0.start()

    def run(self):
        client = Client(client_id="telegram_client")
        client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        client.username_pw_set(username=USERNAME, password=PASSWORD)

        client.connect(host="2de97254567d4bff9dd9184c3910ace3.s1.eu.hivemq.cloud", port=8883)
        client.on_connect = self.mqtt_connect
        client.subscribe('node/jobs')
        
        client.on_message = self.mqtt_onmessage

        client.loop_forever()

    def mqtt_connect(self, broker, userdata, flags, rc):
        print(f"MQTT: connesso al broker, result code: {str(rc)}")

    def mqtt_onmessage(self, client, userdata, msg):
        # time.sleep(1)
        payload = msg.payload.decode("utf-8")
        self.queue.put(payload)
        #print("Messaggio ricevuto: " + msg.topic + " -> " + payload)
        print("Messaggio ricevuto dal topic: " + msg.topic)
        # return payload

# -------------------------------------------- CLASSE BOT TELEGRAM ----------------------------------------------------------
class TelegramBot(object):
    def __init__(self, token, client, my_queue):
        self.token = token
        self.client = client
        self.queue = my_queue
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
        print(f"{user.first_name} sta cercando un posto per {job}")

        update.message.reply_text(f'Grazie {user.first_name}, inviami ora la posizione in cui effettuare la ricerca')
        return LOCATION

    # comando per aggiungere la posizione dell'utente -----------------------------------------------------------------------
    def location(self, update, context):
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

    # Comando per l'invio dei valori ----------------------------------------------------------------------------------------
    def send(self, update, context):

        payload = context.user_data
        str_payload = json.dumps(payload)
        print(str_payload)      # test
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
        payload = self.queue.get()
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

        job_handler = CommandHandler("lavori", self.job_message)

        self.disp.add_handler(start_handler)
        self.disp.add_handler(update_handler)
        self.disp.add_handler(job_handler)

        # avvio del bot, resta in esecuzione fino ad quando non
        #riceve un CTRL+C, SIGTERM O SIGABRT
        self.upd.start_polling()

# ------------------------------------------- MAIN -----------------------------------------------------------------------
def main():

    #global client
    my_queue = Queue()


    client = MQTTClient(USERNAME, PASSWORD, my_queue)
    bot = TelegramBot(TOKEN, client, my_queue)

    # avvio del bot

if __name__ == "__main__":
    main()