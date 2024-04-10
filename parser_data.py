import datetime
from bs4 import BeautifulSoup
import json
import requests
from fake_useragent import UserAgent
from progress.bar import IncrementalBar
from progress.spinner import Spinner
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

chat = GigaChat(credentials="Ваш GigaChatToken", scope="GIGACHAT_API_PERS", verify_ssl_certs=False, streaming=True)

def import_text(link):
    page = requests.get(link).text
    soup = BeautifulSoup(page)
    p_tags = soup.find_all("p")
    #Обработка данных
    p_tags_text = [tag.get_text().strip() for tag in p_tags]
    sentence_list = [sentence for sentence in p_tags_text if not '\n' in sentence]
    sentence_list = [sentence for sentence in sentence_list if '.' in sentence]
    # комбинирование полученных данных в одну str переменную
    article = ' '.join(sentence_list)
    return article

def generate_answer(text):
    messages = [
    SystemMessage(
        content=""
        )
    ]
    messages.append(HumanMessage(content= "Сосотавь вопрос по тексту: "+text))
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
            text = file[i+1]
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

ua = UserAgent()

headers = {
    'accept': 'application/json, text/plain, */*',
    'user-Agent': ua.google,
}

article_dict = {}
num = int(input("Введите количество ссылок: "))
bar = IncrementalBar('Парсинг ссылок', max = num)
a = 0
if num > 1:
    for i in range(num):
        link = f"https://habr.com/ru/articles/page{i}/"
        req = requests.get(link, headers=headers).text

        soup = BeautifulSoup(req, 'lxml')
        all_hrefs_articles = soup.find_all('a', class_='tm-title__link') # получаем статьи
        for article in all_hrefs_articles: # проходимся по статьям
            a += 1
            article_name = article.find('span').text # собираем названия статей
            article_link = f'https://habr.com{article.get("href")}' # ссылки на статьи
            article_dict[article_name] = article_link
            article_dict[a] = article_link
        bar.next()
    bar.finish()
else:
    print(NameError("Слишком малое кол-во ссылок"))
        

not_filter_bar = IncrementalBar('Парсинг ссылок', max = len(article_dict))
count = 1
data = {}

for i in range(len(article_dict)):
    if i > (len(article_dict)//2)-1:
       break
    else:
        if import_text(article_dict[i+1]) != "" and len(import_text(article_dict[i+1])) > 20:
            data[count] = import_text(article_dict[i+1])
            count += 1
        not_filter_bar.next()
not_filter_bar.finish()

with open(f"notFilterData/NotFilterData{datetime.date.today()}.json", "a", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.write("\n")

dataset = split_text(data)
    
with open("dataset.json", "a", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=4)
    f.write("\n")
