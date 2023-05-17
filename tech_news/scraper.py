import requests
import time
from parsel import Selector


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
    URLsNews = selector.css(".entry-header h2 a::attr(href)").getall()
    return URLsNews
    # A url está no atributo href em um elemento âncora (<a>)
    # Dentro de um h2 em elementos que possuem classe entry-header


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    URLButtonNext = selector.css(".next.page-numbers::attr(href)").get()
    return URLButtonNext


# html = fetch("https://blog.betrybe.com/")
# scrape = scrape_next_page_link(html)
# print(scrape)


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
