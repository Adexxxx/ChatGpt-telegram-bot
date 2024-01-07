from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from ChatGPT import gpt
    
TOKEN = 'YOUR_TOKEN'        #Токен телеграм бота
bot = Bot(TOKEN)
dp = Dispatcher(bot)
    

@dp.message_handler(commands='start')            #Обработка команды /start
async def start(message: Message):
    await message.answer('Привет, это чат-бот на основе модели gpt 3.5🔥\nПриступим!')


@dp.message_handler(content_types=types.ContentType.TEXT)        #Любой текст = запрос к chatgpt. 
async def mes(message: types.Message): 
    await message.answer('Генерируется ответ♻️')            #Даём понять пользователю, что бот работает
    await message.reply(gpt(message.text)) # type: ignore        Тут запрос принимается, отдаётся на обработку и выводится
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)        #Удаляем первое сообщение. Только для эстетики
    
if __name__ == '__main__':            #Запускаем проверку поступающих в бота сообщений.
    executor.start_polling(dp)
