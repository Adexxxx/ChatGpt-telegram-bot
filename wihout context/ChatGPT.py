from openai import OpenAI

client = OpenAI(api_key='YOUR_API_KEY')

def gpt(text):
    completion = client.chat.completions.create(
    model = 'gpt-3.5-turbo',                            #Модель можно выбрать на свой вкус
    messages = [
        {"role": "system", "content" : "You are a bot assistant imitating a real person."},        #Тут задаётся личность нейросети. Натсраивается по своему усмотрению (на английском языке) 
        {'role': 'user', 'content': f'{text}'}                                     #Запрос от пользователя, который и обрабатывает нейросеть
    ],
    temperature = 0.5                    #Количество вольности нейросети от 0 до 1. Чем больше, тем больше выразительности и воды
    )
    
    english_text = completion.choices[0].message.content
    
    return english_text
