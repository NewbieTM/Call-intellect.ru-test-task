from code.fetch_news import fetch_latest_news
from code.gigachat_auth import get_token
from code.blog_text_generator import create_blog_text_generator, generate_blog_text
from code.slogan_generator import create_slogan_generator, generate_slogan
from code.image_generator import Text2ImageAPI
from langchain_community.chat_models import GigaChat
from code.file_saver import save_text_to_docx, save_text_to_txt, create_output_directory
from deep_translator import GoogleTranslator

# Set up parameters
AUTH = 'YmE5ZTA1ZTAtOTI0Ny00Y2RkLTk5OGYtNDU4NWQ4NzEyMTE5OjZiYjc4MjY1LTMzZWEtNGE5OC05ODg4LTRiNjQ4M2EyNGFjMQ=='
API_KEY = 'AA553B4C0D1679C81FD4161CF9DE36A3'
SECRET_KEY = 'A9358BEBFAFE9BCB1788DEBD40DF0982'
keywords = ['дети', 'обучение']

# Fetch news
news_list = fetch_latest_news(keywords)

# Authenticate
response = get_token(AUTH)
giga_token = response.json()['access_token']

# Generate blog text
create_output_directory()
chat = GigaChat(verify_ssl_certs=False, scope="GIGACHAT_API_PERS", access_token=giga_token)
blog_text_generator = create_blog_text_generator(chat)
generated_text = generate_blog_text(blog_text_generator, news_list[6]['summary'])
save_text_to_docx(generated_text, "outputs/blog_text.docx")

# Generate slogan
slogan_generator = create_slogan_generator(chat)
slogan = generate_slogan(slogan_generator, generated_text)
save_text_to_txt(slogan, "outputs/image_text.txt")

# Generate image
print("Ожидайте генерации картинки")
api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
model_id = api.get_model()
translated_slogan = GoogleTranslator(source='ru', target='en').translate(slogan)
uuid = api.generate_image(f"A detailed and visually compelling image representing the theme of\
    {translated_slogan} with intricate textures,\
    no text, and an realistic visual style.", model_id)
image_base64 = api.check_generation(uuid)
if image_base64:
    api.save_image(image_base64, "outputs/image.png")
print('Картинка сгенерирована')