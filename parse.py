from bs4 import BeautifulSoup
import requests


# Spiegel
def parse_list_spiegel():
    result = {}
    scr = requests.get("https://www.spiegel.de/international/europe/").text
    soup = BeautifulSoup(scr, "lxml")
    full_info = soup.find_all("div", {"data-area": "article_teaser>news-m-wide"})
    for item in full_info[:5]:
        name = item.find_all("h2", class_="w-full")[0].find("span", class_="align-middle").text
        link = item.find_all("h2", class_="w-full")[0].find("a").get("href")
        result[name] = link
    return result


def parse_text_spiegel(name, url):
    result = ""
    if url == "": url = parse_list_spiegel().get(name)
    scr = requests.get(url).text
    soup = BeautifulSoup(scr, "lxml")
    full_text = soup.find_all("main", {"id": "Inhalt"})[0].find_all("div", {"data-sara-click-el": "body_element",
                                                                            "data-area": "text"})
    for item in full_text:
        result += item.text.strip()
    return result


# Bild
def parse_list_bild():
    result = {}
    scr = requests.get("https://www.bild.de/politik/ausland.html").text
    soup = BeautifulSoup(scr, "lxml")

    full_text = soup.find("main", {"id": "main"}).find("div", "layout layout-9 layout-9--desktop")

    for item in list(full_text)[1:]:
        link = "https://bild.de" + item.find("a").get("href")
        if "bild-plus" not in link:
            name = item.find("div", "teaser__title").find("span", "teaser__title__headline").text
            result[name] = link
    return result


def parse_text_bild(name, url):
    result = ""
    if url == "": url = parse_list_bild().get(name)
    scr = requests.get(url).text
    soup = BeautifulSoup(scr, "lxml")
    full_text = soup.find("main", {"id": "main"}).find("div", "article-body").find_all("p")
    for item in full_text:
        result += item.text.strip()
    return result


# BBC
def parse_list_bbc():
    result = {}
    scr = requests.get("https://www.bbc.com/news/topics/c1vw6q14rzqt").text
    soup = BeautifulSoup(scr, "lxml")
    full_text = soup.find_all("div", {"data-testid": "promo"})
    for item in full_text[:5]:
        link = "https://bbc.com" + item.find("a").get("href")
        name = item.find("span", {"role": "text"}).text
        result[name] = link
    return result


def parse_text_bbc(name, url):
    result = ""
    if url == "": url = parse_list_bbc().get(name)
    scr = requests.get(url).text
    soup = BeautifulSoup(scr, "lxml")
    full_text = soup.find("main", {"id": "main-content"}).find_all("div", {"data-component": "text-block"})
    for item in full_text:
        result += item.text.strip()
    return result


# CNN
def parse_list_cnn():
    result = {}
    scr = requests.get("https://edition.cnn.com/world/europe").text
    soup = BeautifulSoup(scr, "lxml")
    full_text = soup.find("div",
                          class_="container__field-links container_lead-plus-headlines-with-images__field-links").find_all(
        "a")
    for item in full_text[1::2]:
        link = "https://edition.cnn.com" + item.get("href")
        name = item.text.strip()
        result[name] = link
    return result


def parse_text_cnn(name, url):
    result = ""
    if url == "": url = parse_list_cnn().get(name)
    scr = requests.get(url).text
    soup = BeautifulSoup(scr, "lxml")
    full_text = soup.find("main", class_="article__main").find("div", class_="article__content").find_all("p")
    for item in full_text:
        result += item.text.strip()
    return result


# The Daily Telegraph
def parse_list_telegraph():
    result = {}
    scr = requests.get("https://www.telegraph.co.uk/russia-ukraine-war/").text
    soup = BeautifulSoup(scr, "lxml")
    full_text = soup.find("section", class_="article-list-hero").find_all("li")
    for item in full_text[1:6]:
        name = item.find("h2").text.strip()
        link = "https://telegraph.co.uk" + item.find("a").get("href")
        result[name] = link
    return result


def parse_text_telegraph(name, url):
    result = ""
    if url == "": url = parse_list_telegraph().get(name)
    scr = requests.get(url).text
    soup = BeautifulSoup(scr, "lxml")
    full_text = soup.find("div", {"itemprop": "articleBody", "data-js": "article-body"}).find_all("div",
                                                                                                  "article-body-text")
    for item in full_text:
        full = item.find_all("p")
        for part in full:
            result += part.text.strip()
    return result