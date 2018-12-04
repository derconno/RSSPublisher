import pickle

secret = '123456789'
ip = '127.0.0.1'
port = 8000
title = 'RSS Server Event Feed'
link = 'https://conno.ddns.net/'
description = 'This is the event feed of the server. It collects the events of different applications and publishes them here.'


def get_items():
    try:
        f = open('items', 'rb')
        items = pickle.load(f)
        f.close()
    except:
        items = []
    return items


def save_items(items):
    f = open('items', 'wb')
    pickle.dump(items, f)
    f.close()
