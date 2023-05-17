import requests
import time
from parsel import Selector
from bs4 import BeautifulSoup
import re


# Requisito 1
def fetch(url):
    time.sleep(1)  # para a req aguardar 1 seg em cada req que fizer
    try:
        response = requests.get(
            url, timeout=3, headers={"user-agent": "Fake user-agent"})
        if response.status_code == 200:  # caso a req for ok retorna o text
            return response.text
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)
    URLs_news = selector.css(".entry-header h2 a::attr(href)").getall()
    return URLs_news
    # A url está no atributo href em um elemento âncora (<a>)
    # Dentro de um h2 em elementos que possuem classe entry-header


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    URL_button_next = selector.css(".next.page-numbers::attr(href)").get()
    return URL_button_next


# Requisito 4
def scrape_news(html_content):
    selector = Selector(text=html_content)
    soup = BeautifulSoup(html_content, 'html.parser')

    url = selector.css("link[rel=canonical]::attr(href)").get()
    get_title = selector.css("h1::text").get()
    title_clean = re.sub(r'\s+$', '', get_title)
    # expressao regular para remover espacos vazios ao final da string
    # vem da biblioteca re

    timestamp = selector.css(".meta-date::text").get()
    writer = selector.css(".url.fn.n::text").get()
    reading_time = int(selector.css(
        ".meta-reading-time::text").get().split(" ")[0])
    # o split transforma a string em um lista de strings. Retorna apenas
    # o primeiro elemento da lista

    get_summary = soup.find('p').text
    summary_clean = re.sub(r'\s+$', '', get_summary)
    category = selector.css(".label::text").get()

    return {
        "url": url,
        "title": title_clean,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary_clean,
        "category": category,
    }


html = fetch("https://blog.betrybe.com/tecnologia/site-responsivo/")
scrape = scrape_news(html)
print(scrape)


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
