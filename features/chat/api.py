from time import sleep

clients = []
chatHistory = []


def gen():
    q = []
    clients.append(q)

    try:
        while True:
            sleep(0.07)
            if len(q) > 0:
                print(q[0])
                yield f"data: {q.pop(0)}\n\n"
            else:
                yield ": heartbeat\n\n"

    finally:
        clients.remove(q)


def getChatGen():
    return gen()


def getChatHistory():
    return chatHistory


def sendMessage(message):
    chatHistory.append(message)

    for q in clients:
        print("appeneded")
        q.append(message)
