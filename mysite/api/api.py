import time
from django.http import HttpResponse
from pyrogram import Client
from pyrogram.api import functions, types
from pyrogram.api.errors import FloodWait


def getMessages(request, user):
    app = Client(
        "my_account",
        api_id=255229,
        api_hash="97eaaf0eed893b617612bf74d39b6a1d"
    )
    target = user  # "me" refers to your own chat (Saved Messages)
    messages = []  # List that will contain all the messages of the target chat
    offset_id = 0  # ID of the last message of the chunk

    app.start()

    while True:
        try:
            m = app.get_history(target, offset_id=offset_id, limit=10)
        except FloodWait as e:
            # For very large chats the method call can raise a FloodWait
            print("waiting {}".format(e.x))
            time.sleep(e.x)  # Sleep X seconds before continuing
            continue

        if not m.messages:
            break

        messages += m.messages
        offset_id = m.messages[-1].message_id
    app.stop()
    return HttpResponse(messages)
    