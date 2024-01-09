from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from ChatGPT import gpt
import sqlite3
import threading
    
TOKEN = 'YOUR_API_KEY'
bot = Bot(TOKEN)            
dp = Dispatcher(bot)


def create_table():                        # Создаём бд, если её ещё нет
    connect = sqlite3.connect('gpt_us.db')
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


@dp.message_handler(commands='start')            # Обработка команды /start
async def start(message: Message):
    connect = sqlite3.connect('gpt_us.db')        # Подключаемся к бд
    cursor = connect.cursor()
    sql_query = f"""
                            SELECT * FROM ChatGPT WHERE id = '{int(message.chat.id)}'
                            """
    user = cursor.execute(sql_query).fetchone()
    
    if user == None:        # Проверяем, есть ли юзер в бд. Добавляем
        sql_query = f"INSERT INTO ChatGPT(id, con, con2) VALUES ('{message.from_user.id}', '', '')"
        cursor.execute(sql_query)
         
    await message.answer('Привет, это чат-бот на основе модели gpt 3.5🔥\nПриступим!')     # Приветствуем

    connect.commit()        # Закрываем бд
    connect.close()


@dp.message_handler(commands='reset')    # Функция отчистки контекста в бд. 
async def reset(message: Message):    
    connect = sqlite3.connect('gpt_us.db')
    cursor = connect.cursor()
    sql_query = f"UPDATE ChatGPT SET con = '', con2 = '' WHERE id = {message.from_user.id}"
    cursor.execute(sql_query)  
    
    await message.answer('✅История диалога отчищена✅')
    
    connect.commit()
    connect.close()


@dp.message_handler(content_types=types.ContentType.TEXT)        # Обрабатываем запрос
async def mes(message: types.Message): 
    thread = threading.Thread(target=gpt, args=(message.text, message.from_user.id, message.message_id))        # Запускаем в новом потоке обработчик
    thread.start()
       
    
if __name__ == '__main__':
    create_table()
    executor.start_polling(dp)
