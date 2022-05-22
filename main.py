import asyncio
from pyrogram import Client, filters
import config
import DataBase as db

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

app = Client(name="Mitorane", api_id=config.appApiId, api_hash=config.appApiHash)
delay = 30
adminID = "397297425"
flag = False


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

async def send():
    while flag:
        errorCount = 0
        messageCount = 0
        count = 0

        for chat in db.getAllChats():
            try:
                if flag == False :
                    break
                await app.send_message(chat[2], chat[3])

                db.changeMessage(chat[2], chat[4] + 1, chat[5])
                messageCount += 1

                await bot.send_message(adminID, f"Отправлено сообщение в чат - {chat[1]}")
                await asyncio.sleep(delay)
            except Exception as exc:

                await bot.send_message(adminID, f"Ошибка отправки в чат - {chat[1]} \n\n{exc}")
                db.changeMessage(chat[2], chat[4], chat[5] + 1)
                errorCount += 1
                await asyncio.sleep(delay)

        count += 1
        await bot.send_message(adminID, f"Прошел - {count} круг\nОтправлено сообщений - {messageCount}\nНедоставленные сообщение - {errorCount}\n")



@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, """
    КОМАНДЫ:
    
    /botstart [time_seconds] - начать рассылку.
    
    /botstop - закончить рассылку.
    
    /allchats - показывает все добавленные чаты.
    
    /add [user_name] [text] - добавляет чат.
    
    /remove [id  AND  chatID] - удаляет чат.
    
    """)

@dp.message_handler(commands=["botstart"])
async def process_start_command(message: types.Message):
    msg = message.text.split(" ")

    try:
        global delay
        delay = int(msg[1])

        global flag
        flag = True

        await app.start()
        await app.run(await send())

        await bot.send_message(message.from_user.id, "Рассылка запушена")
    except:
        await bot.send_message(message.from_user.id, "Ошибка")



@dp.message_handler(commands=["botstop"])
async def process_start_command(message: types.Message):
    global flag
    flag = False

    await app.stop()
    await bot.send_message(message.from_user.id, "Рассылка приостановлена")



@dp.message_handler(commands=["allchats"])
async def process_start_command(message: types.Message):
    try:
        text = ""

        for chat in db.getAllChats():
            text += f"--------\nChat db_ID:  {chat[0]}\nChat name:  {chat[1]}\nChat id:  {chat[2]}\nChat message count:  {chat[4]}\nChat error message count:  {chat[5]}\n\nChat TEXT:\n{chat[3]}\n--------\n\n\n"
        await bot.send_message(message.from_user.id, text)
    except:
        await bot.send_message(message.from_user.id, "Ошибка")

@dp.message_handler(commands=["add"])
async def process_start_command(message: types.Message):
    try:
        msg = message.text.split(" ")
        chatId = db.getChatId(username=msg[1])

        if chatId != 0:
            db.addChat(chat_id=chatId, chatLink=msg[1], text=msg[2])
            await bot.send_message(message.from_user.id, f"Добавил чат - {msg[1]}\n\nТекст:\n {msg[2]}")
            await bot.send_message(message.from_user.id, f"Что бы удалить этот чат: /remove {chatId}")
        else:
            await bot.send_message(message.from_user.id, "Ошибка юзернейма, юзернейм не правильно набран")
    except:
        await bot.send_message(message.from_user.id, "Ошибка. Возможно этот чат уже добавлен")

@dp.message_handler(commands=["remove"])
async def process_start_command(message: types.Message):
    try:
        msg = message.text.split(" ")
        delete = db.removeChat(msg[1])

        if delete:
            await bot.send_message(message.from_user.id, f"Успешно удален чат с ID:  {msg[1]}")
        else:
            await bot.send_message(message.from_user.id, f"Не смог удалить чат с ID: {msg[1]} \n\n Возможно он уже удален")
    except:
        await bot.send_message(message.from_user.id, f"Что-то пошло не так, попробуйте позже")

@dp.message_handler()
async def echo_message(message: types.Message):
    await bot.send_message(message.from_user.id, """
    КОМАНДЫ:
    
    /botstart [time_seconds] - начать рассылку.
    
    /botstop - закончить рассылку.
    
    /allchats - показывает все добавленные чаты.
    
    /add [user_name] [text] - добавляет чат.
    
    /remove [id  AND  chatID] - удаляет чат.
    
    """)

if __name__ == '__main__':
    executor.start_polling(dp)