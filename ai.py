from langchain.prompts import load_prompt
from langchain.chat_models.gigachat import GigaChat
import arxiv
import config

credentials = 'ZmI3NGRjMDYtNTFjMC00NjdhLTljODgtNTBhOWVjMjk4M2VhOmU2NWY4YjQ2LWEwMGUtNDJjMy1iYmM5LTM0NTJkNGU0OTY3NA=='

chat = GigaChat(model="GigaChat-Pro", credentials=credentials,scope='GIGACHAT_API_CORP', verify_ssl_certs=False)

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