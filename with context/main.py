from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from ChatGPT import gpt
import sqlite3
import asyncio
import threading
import requests
    
TOKEN = '6702860791:AAHXXeO5rBW_hhbC5f3EZaHQpl5XI4mitww'
bot = Bot(TOKEN)
dp = Dispatcher(bot)
i = 0

def create_table():
    connect = sqlite3.connect('C:\\pythonProject\\cgpt_bot\\gpt_us.db')
    cursor = connect.cursor()

    sql_query = """
                    CREATE TABLE IF NOT EXISTS ChatGPT (
                    id INT,
                    con TEXT,
                    con2 TEXT
                    )
                    """
    cursor.execute(sql_query)
    connect.commit()
    connect.close()    


@dp.message_handler(commands='start')
async def start(message: Message):
    connect = sqlite3.connect('C:\\pythonProject\\cgpt_bot\\gpt_us.db')
    cursor = connect.cursor()
    sql_query = f"""
                            SELECT * FROM ChatGPT WHERE id = '{int(message.chat.id)}'
                            """
    user = cursor.execute(sql_query).fetchone()
    
    if user == None:
        sql_query = f"INSERT INTO ChatGPT(id, con, con2) VALUES ('{message.from_user.id}', '', '')"
        cursor.execute(sql_query)
    
    with open('C:\\pythonProject\\cgpt_bot\\gptu.txt', 'a', encoding='utf-8') as file:
        user = message.from_user
        file.write(f'Имя: "{user.first_name}"; Фамилия: "{user.last_name}"; тег: "@{user.username}"; время: {message.date}; id: {message.from_user.id}"\n')
        
    await message.answer('Привет, это чат-бот на основе модели gpt 3.5🔥\nПриступим!')

    connect.commit()
    connect.close()


@dp.message_handler(commands='reset')
async def reset(message: Message):    
    connect = sqlite3.connect('C:\\pythonProject\\cgpt_bot\\gpt_us.db')
    cursor = connect.cursor()
    sql_query = f"UPDATE ChatGPT SET con = '', con2 = '' WHERE id = {message.from_user.id}"
    cursor.execute(sql_query)  
    
    await message.answer('✅История диалога отчищена✅')
    
    connect.commit()
    connect.close()


@dp.message_handler(content_types=types.ContentType.TEXT)
async def mes(message: types.Message): 
    
    
    # await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    # try:
    thread = threading.Thread(target=gpt, args=(message.text, message.from_user.id, message.message_id))
    thread.start()
        # await message.reply(gpt(message.text, message.from_user.id), parse_mode="Markdown") # type: ignore
    # except:
    #     await message.reply('❌ Не так быстро. Слишком много запросов, попробуй снова через 30 секунд')

    # msg = await message.answer('Генерируется ответ♻️')
    # await message.reply(gpt(message.text, message.from_user.id), parse_mode="Markdown") # type: ignore
    # await msg.delete()
    
    
# async def rep(message: types.Message):
#     url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={message.from_user.id}&text=обработка началась&reply_to_message_id={message.message_id}"
#     data = requests.get(url).json()
#     msg = await message.answer('Генерируется ответ♻️')
#     await bot.send_chat_action(chat_id=message.chat.id, action="typing")
#     try:
#         await message.reply(gpt(message.text, message.from_user.id), parse_mode="Markdown") # type: ignore
#     except:
#         await message.reply('❌ Не так быстро. Слишком много запросов, попробуй снова через 30 секунд')

#     await msg.delete()   
    
if __name__ == '__main__':
    create_table()
    executor.start_polling(dp)
    
    
    
    # нужен многопоток. очень. и, наверно, всё.
    # отправка и удлаение сообщений через реквест есть, отсалось запихать это в потоки