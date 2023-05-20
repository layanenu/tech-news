import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1 - Pega o conteudo html da pag
def fetch(url):
    time.sleep(1)  # para a req aguardar 1 seg em cada req que fizer
    try:
        response = requests.get(
            url, timeout=3, headers={"user-agent": "Fake user-agent"})
        if response.status_code == 200:  # caso a req for ok retorna o text
            return response.text
    except requests.ReadTimeout:
        return None


# html = fetch("https://blog.betrybe.com/")
# print(html)


# Requisito 2 - pega a url da noticia
def scrape_updates(html_content):
    selector = Selector(text=html_content)
    URLs_news = selector.css(".entry-header h2 a::attr(href)").getall()
    return URLs_news
    # A url está no atributo href em um elemento âncora (<a>)
    # Dentro de um h2 em elementos que possuem classe entry-header


# Requisito 3 - pega a url do botao proximo
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    URL_button_next = selector.css(".next.page-numbers::attr(href)").get()
    return URL_button_next


# Requisito 4
def scrape_news(html_content):
    selector = Selector(text=html_content)
    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css("h1::text").get().strip()
    timestamp = selector.css(".meta-date::text").get()
    writer = selector.css(".author a::text").get()
    reading_time = int(selector.css(".meta-reading-time::text")
                       .get().split(" ")[0])
    summary = "".join(selector.css(".entry-content > p:nth-of-type(1) *::text")
                      .getall()).strip()
    category = selector.css(".label::text").get()

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary,
        "category": category,
    }


# Requisito 5
def get_tech_news(amount):
    url = "https://blog.betrybe.com/"
    contador = 0
    news = []

    while contador < amount:
        html_content = fetch(url)
        urls = scrape_updates(fetch(url))

        for url in urls:
            html_content_article = fetch(url)
            news.append(scrape_news(html_content_article))
            contador += 1
            if contador == amount:
                break
        url = scrape_next_page_link(html_content)

    create_news(news)
    return news
