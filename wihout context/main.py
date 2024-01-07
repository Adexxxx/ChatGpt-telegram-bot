from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from ChatGPT import gpt
    
TOKEN = '6702860791:AAHXXeO5rBW_hhbC5f3EZaHQpl5XI4mitww'
bot = Bot(TOKEN)
dp = Dispatcher(bot)
    

@dp.message_handler(commands='start')
async def start(message: Message):
    with open('C:\\pythonProject\\cgpt_bot\\gptu.txt', 'a', encoding='utf-8') as file:
        user = message.from_user
        file.write(f'Имя: "{user.first_name}"; Фамилия: "{user.last_name}"; тег: "@{user.username}"; время: {message.date}; id: {message.from_user.id}"\n')
    await message.answer('Привет, это чат-бот на основе модели gpt 3.5🔥\nПриступим!')


@dp.message_handler(content_types=types.ContentType.TEXT)
async def mes(message: types.Message): 
    await message.answer('Генерируется ответ♻️')
    await message.reply(gpt(message.text)) # type: ignore
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
    
if __name__ == '__main__':
    executor.start_polling(dp)