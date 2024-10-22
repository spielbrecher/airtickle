from langchain.prompts import load_prompt
from langchain.chat_models.gigachat import GigaChat
import arxiv
import config

# credentials = 'ZmI3NGRjMDYtNTFjMC00NjdhLTljODgtNTBhOWVjMjk4M2VhOmU2NWY4YjQ2LWEwMGUtNDJjMy1iYmM5LTM0NTJkNGU0OTY3NA=='
credentials = 'ZmI3NGRjMDYtNTFjMC00NjdhLTljODgtNTBhOWVjMjk4M2VhOjYyMGVlNmMzLTExMjQtNGE4Zi05M2NiLWY4N2MxODk5MDA5Yw=='

chat = GigaChat(model="GigaChat", credentials=credentials,scope='GIGACHAT_API_PERS', verify_ssl_certs=False)

def create_hypothesis():
    prompt = load_prompt("scientist_hypothesis.yaml")
    chain = prompt | chat
    hypothesis = chain.invoke(
        {
            "text": config.artickle_description
        }
    ).content
    return hypothesis

def create_ru_keywords():
    prompt = load_prompt("scientist_keywords.yaml")
    chain = prompt | chat
    keywords = chain.invoke(
        {
            "text": config.artickle_description
        }
    ).content
    return keywords

def translate_keywords():
    prompt = load_prompt("translation_rueng.yaml")
    #prompt = 'Переведи на английский язык ключевые слова. Не пиши ничего лишнего. Только перевод ключевых слов на английском языке'
    chain = prompt | chat
    translated_keywords = chain.invoke(
        {
            "text": config.keywords
        }
    ).content
    return translated_keywords

def create_plan():
    # Создаем план работы над статьей
    prompt = load_prompt("scientist_plan.yaml")
    chain = prompt | chat
    plan = chain.invoke(
        {
            "text": config.artickle_description
        }
    ).content
    return plan

def get_literature():
    # Construct the default API client.
    client = arxiv.Client()

    # Search for the most recent articles
    search = arxiv.Search(
        query=config.translated_keywords,
        max_results=20,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    results = client.results(search)
    all_results = list(results)
    return all_results

def save_pdf(num):
    paper = config.literature[num]
    paper.download_pdf(dirpath=".")