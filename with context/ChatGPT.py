from openai import AsyncOpenAI
import sqlite3
import re

client = AsyncOpenAI(api_key='YOUR_OPENAI_API_KEY')


async def gpt(text: str, user_id: int) -> str | bool:
    try:
        """Подключаемся к бд, чтобы достать последние два ответа бота. Они будут нужны для чат гпт"""

        connect = sqlite3.connect("gpt_us.db", check_same_thread=False)
        cursor = connect.cursor()
        result = cursor.execute("SELECT con, con2 FROM ChatGPT WHERE id = ?", (user_id,)).fetchone()
        if result:
            con = result[0]
            con2 = result[1]
        else:
            con = ""
            con2 = ""

        """
        Передаём инфу к чат гпт
        
        Поле "model" версию можно менять по своему усмотрению
        В поле "role:system" в content указываем "личность" бота на английском языке
        В поле "role:user" в content передаем текст запроса от пользователя
        В поле "role:assistant" в content передаём контекст - последние два ответа бота
        Поле "temperature" отвечает за количество выразительности ответа. Значение от 0 до 1. 
        """

        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "chipi chipi chapa chapa"},
                {"role": "user", "content": f"{text}"},
                {"role": "assistant", "content": f"{con} {con2}"}
            ],
            temperature=0.9
        )
        ppp = re.compile("[a-zA-Z]")  # Нужно для проверки дальше
        
        english_text = completion.choices[0].message.content  # Получаем ответ нейросети на сообщение пользователя
        if ppp.match(english_text):  # Проверяем язык ответа, если Английский запрашиваем повторно без контекста
            completion = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "chipi chipi chapa chapa"},
                    {"role": "user", "content": f"{text}"}
                ],
                temperature=0.9
            )
            english_text = completion.choices[0].message.content

        try:
            """После обработки запроса, обновляем ответы для контекста в бд"""

            cursor.execute(
                "UPDATE ChaTGPT SET con = ?, con2 = ? WHERE id = ?",
                (english_text, con, user_id)
            )
        except sqlite3.OperationalError:  # На случай ошибок
            cursor.execute(
                "UPDATE ChaTGPT SET con = ?, con2 = ? WHERE id = ?",
                ("", con, user_id)
            )
        connect.commit()  # Сохраняем и закрываем бд
        connect.close()
        
        return english_text
    except Exception as ex:  # На случай превышения лимитов запросов к api
        print(ex)
        return False
