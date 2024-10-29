import datetime
from bs4 import BeautifulSoup
import json
import requests
from fake_useragent import UserAgent
from progress.bar import IncrementalBar
from progress.spinner import Spinner
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

chat = GigaChat(credentials="MDM1YjkzNjItMzhkYS00NTRkLWI1MzUtOTg5NmZhMjFkYzljOjZlZTVkZjJhLTIxZGYtNDQ5MS05MzZjLTIxNjQ3ODcwMTZmZA==", scope="GIGACHAT_API_PERS", verify_ssl_certs=False, streaming=True)

file = "notFilterData/NotFilterData2024-10-17.json"

with open(file, "r", encoding="utf-8") as f:
    data = json.loads(f.read())

def generate_answer(text):
    messages = [
    SystemMessage(
        content=""
        )
    ]
    messages.append(HumanMessage(content= "Составь вопрос по тексту: "+text))
    res = chat(messages)
    messages.append(res)
    return res.content

def split_text(file):
    json_dict = []
    for i in range(len(file)):
        if i > len(file)//2:
            break
        else:
        # Разделение текста на предложения
            text = file[str(i+1)]
            sentences = text.split('. ')
    
    # Разделение предложений на части по 8
            parts = [sentences[i:i+8] for i in range(0, len(sentences), 8)]
    
    # Преобразование частей в строки и запись в словарь
            for part in parts:
                str_var_value = '. '.join(part)
                if str_var_value != "":
                    json_dict.append({
                        "Вопрос": generate_answer(str_var_value),
                        "Ответ": str_var_value})
    
    return json_dict


dataset = split_text(data)

with open(f"data.json", "a", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=4)
    f.write("\n")