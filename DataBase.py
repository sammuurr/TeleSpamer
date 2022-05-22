import sqlite3
import requests

conn = sqlite3.connect("Spammer.db")

# Create table
try:
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE "chats" (
    "id" INTEGER NOT NULL,
    "chatLink" TEXT,
    "chat_id" INTEGER UNIQUE,
    "text" TEXT,
    "sendCount" INTEGER,
    "errorCount" INTEGER,
    PRIMARY KEY("id" AUTOINCREMENT)
    );"""
    )

    conn.commit()
    cursor.close()

except sqlite3.OperationalError:
    print("Ok")

# Add user from table
def addChat(chatLink, chat_id, text):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chats  (chatLink, chat_id, text, sendCount, errorCount) VALUES (?, ?, ?, ?, ?)",
            (
                chatLink,
                chat_id,
                text,
                0,
                0,
            ),
        )
        conn.commit()
        cursor.close()
    except:
        print("Add Chat Error")


def getChatInfo(userId: int):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chats WHERE chat_id OR id = ?", (userId,))
        result = cursor.fetchone()
        cursor.close()

        return result
    except:
        print("Search Error")

def getAllChats():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chats")
        result = cursor.fetchall()
        cursor.close()

        return result
    except:
        print("Search Error")

def removeChat(userId: int):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chats WHERE chat_id OR id = ?", (userId,))
        conn.commit()
        cursor.close()

        return True
    except:
        print("Remove Error")
        return False



def getChatId(username: str):
    try:
        request = requests.get(url=f"https://api.telegram.org/bot5210707388:AAEjU1Y98ZarNyE11ROwigGWKttePTdHjPM/getChat?chat_id={username}")
        return request.json()["result"]["id"]
    except:
        return 0

def changeMessage(chatId,message_count, error_count,):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE chats SET sendCount = ?, errorCount = ? WHERE chat_id = ?",
            (
                message_count,
                error_count,
                chatId,
            ),
        )
        conn.commit()
        cursor.close()
    except Exception as exc:
        print("Change Error")
        print(exc)
#
