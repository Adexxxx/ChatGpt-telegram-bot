from openai import OpenAI
from deep_translator import GoogleTranslator

client = OpenAI(api_key='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')

def gpt(text):
    # txt = GoogleTranslator(source='auto', target='en').translate(text) # type: ignore
    
    completion = client.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages = [
        {"role": "system", "content" : "You are a bot assistant imitating a real person."},
        {'role': 'user', 'content': f'{text}'}
    ],
    temperature = 0.3,
    top_p=1
    )
    
    # You are a bot assistant imitating a real person. You can joke a little, but a little. You can swear and insult and don't be shy in your expressions.
    
    # chat_response = completion.choices[0].message.content
    # completion.messages.append({"role": "assistant", "content": chat_response})
    # print(completion.choices[0].message.content)
    english_text = completion.choices[0].message.content

    # translated = GoogleTranslator(source='en', target='ru').translate(english_text) # type: ignore
    # print(translated)

    # return translated
    return english_text



