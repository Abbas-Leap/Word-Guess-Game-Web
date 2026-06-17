import json
from time import sleep

from flask.json import jsonify

from features.users import api as usersTrackAPI

clients = []


def userStatusGenerator(username):
    q = []

    clients.append(q)
    try:
        while True:
            sleep(0.1)
            if len(q) > 0:
                yield f"data: {json.dumps(q.pop(0))}\n\n"
            else:
                yield ": heartbeat \n\n"
    except GeneratorExit:
        print(f"{username} logged off")
        clients.remove(q)
        usersTrackAPI.removeUserFromActive(username=username)


def getUserStatusGenerator(username):
    return userStatusGenerator(username=username)


def updateUsersStatus():
    print("Updating")

    for q in clients:
        q.append(
            {
                "activeUsers": len(usersTrackAPI.getActiveUsers()["data"]),
                "readyUsers": len(usersTrackAPI.getReadyUsers()["data"]),
            }
        )
