import sqlite3

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from ChatGPT import gpt

TOKEN = "6529393206:AAGiq3RTgwbf7_pk1nK45TVkgo_i14qXEZY"
bot = Bot(TOKEN)
dp = Dispatcher(bot)


def create_table():
    """Создаём бд, если её ещё нет"""

    connect = sqlite3.connect("gpt_us.db", check_same_thread=False)
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS ChatGPT (
                    id INT,
                    con TEXT,
                    con2 TEXT
                    )""")
    connect.commit()
    connect.close()


@dp.message_handler(commands="start")
async def start(message: Message) -> None:
    """Обработчик команды /start"""

    connect = sqlite3.connect("gpt_us.db", check_same_thread=False)
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM ChatGPT WHERE id = ?", (message.from_user.id,))
    user = cursor.fetchone()
    if not user:  # Проверяем, есть ли юзер в бд. Добавляем
        cursor.execute(
            "INSERT INTO ChatGPT VALUES (?, ?, ?)", (message.from_user.id, "", "")
        )

    await message.answer("Привет, это чат-бот на основе модели gpt 3.5🔥\nПриступим!")  # Приветствуем

    connect.commit()  # Закрываем соединение с бд
    connect.close()


@dp.message_handler(commands="reset")
async def reset(message: Message) -> None:
    """Функция отчистки контекста в бд"""

    connect = sqlite3.connect("gpt_us.db", check_same_thread=False)
    cursor = connect.cursor()
    cursor.execute(
        "UPDATE ChatGPT SET con = ?, con2 = ? WHERE id = ?",
        ("", "", message.from_user.id)
    )
    cursor.fetchone()
    connect.commit()
    connect.close()

    await message.answer("✅История диалога отчищена✅")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def mes(message: types.Message) -> None:
    msg_accept = await message.answer(text="Генерируется ответ♻️")
    gpt_answer = await gpt(text=message.text, user_id=message.from_user.id)
    if not gpt_answer:
        await msg_accept.edit_text(
            text="❌ Что-то пошло не так. Попробуй снова через 30 секунд"
        )
        return
    await msg_accept.delete()
    await message.answer(text=gpt_answer)


if __name__ == "__main__":
    create_table()
    executor.start_polling(dp)
