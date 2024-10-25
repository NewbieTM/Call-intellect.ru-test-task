import os
from docx import Document


import warnings
warnings.filterwarnings("ignore")


from langchain_community.chat_models import GigaChat
from langchain_core.messages import SystemMessage 
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain


import requests
from bs4 import BeautifulSoup
import uuid

import json
import time
import base64


from deep_translator import GoogleTranslator


# Задача:
# 
# Необходимо разработать умного ассистента, который выполнит следующие шаги:
# 
# 1. Поиск информации в интернете:
# - Ассистент должен находить в интернете последние новости, связанные с целевой аудиторией - мамами. Основной фокус на новости, касающиеся важности раннего обучения детей арифметике, скорочтению и другим предметам.
# 
# 2. Создание текста для блога:
# - На основе найденной новости ассистент должен создать краткий, но содержательный текст, подходящий для блога. Текст должен быть написан простым и понятным языком, рассчитанным на аудиторию мам.
# 
# 3. Создание текста для изображения:
# - Из текста для блога нужно выделить основную мысль или лозунг, который будет использоваться для создания изображения (например, баннера или инфографики). Текст должен быть кратким и запоминающимся.
# 
# 4. Создание изображения:
# - На основе подготовленного текста для изображения необходимо сгенерировать визуальный контент (изображение). Это может быть простая графика, инфографика или баннер.
# 
# 5. Сохранение результатов:
# - Ассистент должен сохранить следующие файлы:
# - Документ с текстом для блога в формате .docx.
# - Сгенерированное изображение в формате .png или .jpg.
# - Исходный текст для изображения, который использовался при создании графики, в отдельном текстовом файле.
# 
# Требования:
# 
# 1. Ассистент должен быть автономным и автоматически выполнять указанные шаги, начиная с поиска информации и заканчивая сохранением результатов.
# 2. В процессе разработки ассистента необходимо использовать технологию ChatGPT (или аналоги) для генерации текстов на этапах 2 и 3.
# 3. Необходимо предоставить отчет о проделанной работе, где будут описаны:
# - Используемые технологии и библиотеки.
# - Подходы к решению каждой из задач.
# - Возможные улучшения и оптимизации ассистента.
# 
# Ожидаемый результат:
# 
# - Запуск умного ассистента, который выполнит все вышеописанные шаги.
# - Предоставление всех созданных файлов (текст для блога, изображение, исходный текст для изображения).
# - Отчет о проделанной работе.
# 
# Критерии оценки:
# 
# - Корректность выполнения каждого этапа задачи.
# - Качество созданного текста и изображения.
# - Автономность и стабильность работы ассистента.
# - Понимание применяемых технологий и обоснованность их выбора.
# - Креативность в подходе к решению задачи.
# 
# Дополнительных критериев нет, выполните работу по заданным параметрам, как считаете нужным.

# ## 1.1 Первый подход поиска новостей


def fetch_latest_news(keywords):
    url = f"https://www.babyblog.ru/search?request={'+'.join(keywords)}"
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', class_='post-body-content-info')[:25]
    news = []
    for article in articles:
        summary = article.find('p').text
        link = article.find('a')['href']
        news.append({'summary': summary, 'link': f'https://www.babyblog.ru{link}'})
    return news


#keywords = ['раннее обучение', 'дети', 'арифметика', 'скорочтение']
keywords = ['дети', 'обучение']


news_list = fetch_latest_news(keywords)


# ## 2.Построение текста для блога

# Был выбран первый подход для поиска новостей

# ### Получение ключа для Gigachat 


auth = 'YmE5ZTA1ZTAtOTI0Ny00Y2RkLTk5OGYtNDU4NWQ4NzEyMTE5OjZiYjc4MjY1LTMzZWEtNGE5OC05ODg4LTRiNjQ4M2EyNGFjMQ=='



def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    """
      Выполняет POST-запрос к эндпоинту, который выдает токен.
      Возвращает:
      - ответ API, где токен и срок его "годности".
      """
    rq_uid = str(uuid.uuid4())

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    payload = {
        'scope': scope
    }

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1

     


response = get_token(auth)
if response != 1:
  print(response.text)
  giga_token = response.json()['access_token']




chat = GigaChat(verify_ssl_certs=False, scope="GIGACHAT_API_PERS", access_token = giga_token)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="You are an AI assistant who shares everything you know.\
            Based on the text of the article you received, you have to write a\
            text that is written in simple and clear language, aimed at an audience\
            of moms.You have to pretend you don't know the text of the article,\
            i.e. don't respond to the article itself, but create your own,\
            based on the one available. Talks in Russian. Each response must be at least 200 words."
        ),  
        HumanMessagePromptTemplate.from_template(
            "{human_input}"
        ),  
    ]
)

chad = LLMChain(
    llm=chat,
    prompt=prompt,
)



def chat_with_memory(user_input):
    response = chad.predict(human_input=user_input)
    print(f'Оригинальный текст: {user_input} \n\nСгенерированный текст: {response} \n\n')
    return response

generated_texts = []

user_input = news_list[6]['summary']
if user_input:
    ai_respon = chat_with_memory(user_input)
    generated_texts.append(ai_respon)


# ## 3. Создание текста для изображения


chat = GigaChat(verify_ssl_certs=False, scope="GIGACHAT_API_PERS", access_token = giga_token,)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="Из текста для блога нужно извлечь главную мысль\
            или слоган.\
            Текст должен быть кратким и запоминающимся. Свяжите эту главную идею с детской темой.\
            Старайтесь использовать такие слова, как «из детства» и подобные, свойственные детям. Пишите на русском языке"
        ),  
        HumanMessagePromptTemplate.from_template(
            "{human_input}"
        ),  
    ]
)

chad = LLMChain(
    llm=chat,
    prompt=prompt,
)



def chat_with_memory(user_input):
    response = chad.predict(human_input=user_input)
    print(f'Оригинальный текст: {user_input} \n\n\nСгенерированный текст: {response} \n\n\n\n')
    return response

mottoes = []
for text in generated_texts:
    if text:
        ai_respon = chat_with_memory(text)
        mottoes.append(ai_respon)


# ## 4. Создание изображения

# ### 4.2 Второй подход (выбранный)


#!pip install deep-translator

API_KEY = 'AA553B4C0D1679C81FD4161CF9DE36A3'
SECRET_KEY = 'A9358BEBFAFE9BCB1788DEBD40DF0982'



class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=512, height=512):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images'][0]

            attempts -= 1
            time.sleep(delay)

    def save_image(self, image_base64, filename="image.png"):

        image_data = base64.b64decode(image_base64)
        with open(filename, "wb") as file:
            file.write(image_data)



api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
model_id = api.get_model()
for i, motto in enumerate(mottoes):
    print(i,motto)
    translated = GoogleTranslator(source='ru', target='en').translate(motto)
    uuid = api.generate(f"A detailed and visually compelling image representing the theme of\
    {translated} with intricate textures,\
    no text, and an realistic visual style.", model_id)
    image_base64 = api.check_generation(uuid)
    if image_base64:
        api.save_image(image_base64, f"{i}.png")
        print(f"Image saved as {i}.png")
    else:
        print("Image generation failed or timed out")


# Функция для сохранения текста в файл .docx
def save_text_to_docx(text, filename):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)

# Функция для сохранения текста в файл .txt
def save_text_to_txt(text, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)

# Используйте эти функции для сохранения данных
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# Сохраняем текст для блога
if generated_texts:
    save_text_to_docx(generated_texts[0], "outputs/blog_text.docx")
    print("Blog text saved as blog_text.docx")

# Сохраняем исходный текст для изображения
if mottoes:
    save_text_to_txt(mottoes[0], "outputs/image_text.txt")
    print("Image source text saved as image_text.txt")

# Изображение уже сохранено в предыдущей части: api.save_image(image_base64, f"outputs/{i}.png")
