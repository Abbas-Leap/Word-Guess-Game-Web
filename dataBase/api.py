import sqlite3
from pathlib import Path

from logs import api as lg

dbFile = Path(__file__).resolve().parent / "data.db"

usernameChars = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "_",
]

connection = sqlite3.connect(dbFile)

cursor = connection.cursor()

# Check if db table exists and create table if missing
cursor.execute("SELECT name FROM sqlite_master WHERE name='accounts'")
if not cursor.fetchone():
    lg.logInfo("Creating Tables")
    cursor.execute("CREATE TABLE accounts(username, password, points)")
    connection.commit()


#
def validateUsername(username):
    if len(username) > 15 or len(username) < 3:
        return {
            "status": "declined",
            "msg": "Username too long or too short make it between 3 and 15 characters",
        }

    for i in username.lower():
        if i not in usernameChars:
            return {
                "status": "declined",
                "msg": "Invalid Characters use only letters numbers and _",
            }

    return {"status": "ok"}


def createAccount(username, password):
    # Check if account exists (to avoid account reseting / stealing usernames)
    cursor.execute(f"SELECT * FROM accounts WHERE username = '{username}'")

    if cursor.fetchone():
        lg.logInfo(f"Declined account {username} already exists")

        return {"status": "declined", "msg": "Account already exists"}
    # Create account in format Username: [password, points]
    lg.logInfo(f"Creating account {username}")

    cursor.execute(f"""INSERT INTO accounts(username, password, points)
        VALUES ('{username}', '{password}', 0)
        """)

    connection.commit()
    #
    return {"status": "ok"}


def fetchAllAccountData(username):
    cursor.execute(f"SELECT * FROM accounts WHERE username = '{username}'")

    data = cursor.fetchone()

    if not data:
        lg.logInfo(f"Failed to fetch info of account {username} it was not found")
        return {"status": "failed"}

    return {"status": "ok", "data": data}


def addPointsToAccount(username, points):
    # Get points
    cursor.execute(f"""
        SELECT points
        FROM accounts
        WHERE username = '{username}'
        """)

    currentPoints = cursor.fetchone()[0]
    #
    goalPoints = points + currentPoints

    cursor.execute(f"""
        UPDATE accounts
        SET points = {goalPoints}
        WHERE username = '{username}'
        """)

    connection.commit()

    return {"status": "ok"}
