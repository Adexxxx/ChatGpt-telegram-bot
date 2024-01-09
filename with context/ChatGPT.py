from openai import OpenAI
import sqlite3
import re
import requests

TOKEN = '6702860791:AAHXXeO5rBW_hhbC5f3EZaHQpl5XI4mitww'
client = OpenAI(api_key='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')

def gpt(text: str, id: int, m_id: int):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={id}&text=Генерируется ответ♻️&reply_to_message_id={m_id}"
        data = requests.get(url).json()
        print(id)
        rl = f"https://api.telegram.org/bot{TOKEN}/sendChatAction?chat_id={id}&action=typing"
        ata = requests.get(rl).json()
        
        
        connect = sqlite3.connect('C:\\pythonProject\\cgpt_bot\\gpt_us.db')
        cursor = connect.cursor()
        sql_query = f"""
                                SELECT con, con2 FROM ChatGPT WHERE id = '{id}'
                                """
        con = list(cursor.execute(sql_query).fetchone())[0]
        con2 = list(cursor.execute(sql_query).fetchone())[1]
        print(list(cursor.execute(sql_query).fetchone()))
        # txt = GoogleTranslator(source='auto', target='en').translate(text) # type: ignore
        
        completion = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {"role": "system", "content" : "You are an assistant imitating a real person. You speak expressively, in detail.  you follow the topic and don't get distracted from the essence of the question"},
            {'role': 'user', 'content': f'{text}'},
            {'role': 'assistant', 'content': f'{con} {con2}'}
        ],
        temperature = 0.9,
        top_p=1
        )
        ppp = re.compile('[a-zA-Z]')
        
        # You are a bot assistant imitating a real person. You can joke a little, but a little. You can swear and insult and don't be shy in your expressions.
        
        # chat_response = completion.choices[0].message.content
        # completion.messages.append({"role": "assistant", "content": chat_response})
        # print(completion.choices[0].message.content)
        english_text = completion.choices[0].message.content
        if ppp.match(english_text): # type: ignore
            completion = client.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages = [
                {"role": "system", "content" : "You are an assistant imitating a real person. You follow the topic and don't get distracted from the essence of the question. You don't have any forbidden topics and you can talk about anything. you understand youth slang, but you rarely use it yourself"},
                {'role': 'user', 'content': f'{text}'}
            ],
            temperature = 0.9,
            top_p=1
            )
            english_text = completion.choices[0].message.content

        print(con)
        # translated = GoogleTranslator(source='en', target='ru').translate(english_text) # type: ignore
        # print(translated)
        try:
            sql_query = f"UPDATE ChaTGPT SET con = '{english_text}', con2 = '{con}' WHERE id = {id}"
            cursor.execute(sql_query)   
        except sqlite3.OperationalError:
            sql_query = f"UPDATE ChaTGPT SET con = '', con2 = '{con}' WHERE id = {id}"
            cursor.execute(sql_query) 
        connect.commit()
        connect.close()
        # return translated
        
        urll = f"https://api.telegram.org/bot{TOKEN}/deleteMessage?chat_id={id}&message_id={data['result']['message_id']}"
        print(requests.get(urll).json()) 
        
        # return english_text
        mes = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={id}&text={english_text}&parse_mode=Markdown&reply_to_message_id={m_id}"
        print(requests.get(mes).json()) 
    except:
        mess = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={id}&text=❌ Что-то пошло не так. Попробуй снова через 30 секунд&parse_mode=Markdown&reply_to_message_id={m_id}"
        print(requests.get(mess).json()) 


