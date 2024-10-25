from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain

def create_blog_text_generator(chat):
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="Твоя генерация должна быть очень содержательной и информативной\
            Ты должен раскрыть проблему и написать много о том как ты её решил бы\
            Основываясь на тексте полученной вами статьи, вы должны написать\
            текст, написанный простым и понятным языком, ориентированный на аудиторию\
            мам. Говорите на русском языке."
            ),
            HumanMessagePromptTemplate.from_template("{human_input}")
        ]
    )
    return LLMChain(llm=chat, prompt=prompt)

def generate_blog_text(chain, user_input):
    response = chain.predict(human_input=user_input)
    return response
