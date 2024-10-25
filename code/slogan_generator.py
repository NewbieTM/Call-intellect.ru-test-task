from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain

def create_slogan_generator(chat):
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="Из текста для блога нужно извлечь главную мысль\
            или слоган.\
            Текст должен быть кратким и запоминающимся. Свяжите эту главную идею с детской темой.\
            Старайтесь использовать такие слова, как «из детства» и подобные, свойственные детям. Пишите на русском языке"
            ),
            HumanMessagePromptTemplate.from_template("{human_input}")
        ]
    )
    return LLMChain(llm=chat, prompt=prompt)

def generate_slogan(chain, blog_text):
    return chain.predict(human_input=blog_text)
