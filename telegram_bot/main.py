
from queue import Queue

from config import TOKEN, USERNAME, PASSWORD, TOPICS
from MQTTClient import MQTTClient
from TelegramBot import TelegramBot

# ------------------------------------------- MAIN -----------------------------------------------------------------------
def main():

    dict_queues = {}

    for topic in TOPICS:
        queue = Queue()
        dict_queues[topic] = queue

    client = MQTTClient(USERNAME, PASSWORD, TOPICS, dict_queues)
    bot = TelegramBot(TOKEN, client, dict_queues)


if __name__ == "__main__":
    main()