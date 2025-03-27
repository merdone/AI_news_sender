from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


# Spiegel
def parse_list_spiegel():
    result = {}
    scr = requests.get("https://www.spiegel.de/international/europe/").text
    soup = BeautifulSoup(scr, "lxml")
    full_info = soup.find_all("div", {"data-area": "article_teaser>news-m-wide"})
    for item in full_info[:5]:
        name = item.find_all("h2", class_="w-full")[0].find("span", class_="align-middle").text
        link = item.find_all("h2", class_="w-full")[0].find("a").get("href")
        result[link] = name
    return result


def parse_text_spiegel(url):
    result = ""
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
    scr = requests.get("https://www.bild.de/politik/ausland/politik-ausland/home-15683414.bild.html").text
    soup = BeautifulSoup(scr, "lxml")
    full_text = soup.find("main", {"id": "main"}).find("section", {"class": "block block--titled"}).find("div", {
        "class": "layout layout-9 layout-9--desktop"})
    for item in list(full_text)[1:6]:
        link = "https://bild.de" + item.find("a", {"class": "anchor stage-teaser__anchor"}).get("href")
        if "bild-plus" not in link:
            name = item.find("h3", {"class": "teaser__title"}).find("span", {"class": "teaser__title__headline"}).text
            result[link] = name
    return result


def parse_text_bild(url):
    result = ""
    scr = requests.get(url).text
    soup = BeautifulSoup(scr, "lxml")
    full_text = soup.find("main", {"id": "main"}).find("div", "article-body").find_all("p")
    for item in full_text:
        result += item.text.strip()
    return result


# BBC
def parse_list_bbc():
    result = {}
    scr = requests.get("https://www.bbc.com/news/war-in-ukraine").text
    soup = BeautifulSoup(scr, "lxml")
    full_text = soup.find("div", {"data-testid": "undefined-grid-7"}).find_all("div",
                                                                               {"data-testid": "anchor-inner-wrapper"})
    for item in full_text[:5]:
        link = "https://bbc.com" + item.find("a").get("href")
        if "live" in link:
            continue
        name = item.find("h2", {"data-testid": "card-headline"}).text
        result[link] = name
    result = dict(reversed(list(result.items())))
    return result


def parse_text_bbc(url):
    result = ""
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
    full_text = soup.find("div", {"class": "zone zone--t-light"}).find_all("div", {
        "class": "card container__item container__item--type-media-image container__item--type-section container_vertical-strip__item container_vertical-strip__item--type-section"})
    for item in list(full_text)[:5]:
        link = "https://edition.cnn.com" + item.find("a").get("href")
        if "live" in link:
            continue
        name = item.find("span", {"class": "container__headline-text"}).text
        result[link] = name
    return result


def parse_text_cnn(url):
    result = ""
    scr = requests.get(url).text
    soup = BeautifulSoup(scr, "lxml")
    full_text = soup.find("main", class_="article__main").find("div", class_="article__content").find_all("p")
    for item in full_text:
        result += item.text.strip()
    return result


# The Daily Telegraph
def parse_list_telegraph():
    result = {}
    scr = requests.get("https://www.telegraph.co.uk/russia-ukraine-war/", headers=headers).text
    soup = BeautifulSoup(scr, "lxml")
    full_text = soup.find("main", {"id": "main-content"})
    for item in full_text[1:6]:
        name = item.find("h2").text.strip()
        link = "https://telegraph.co.uk" + item.find("a").get("href")
        result[name] = link
    return result


def parse_text_telegraph(url):
    result = ""
    scr = requests.get(url).text
    soup = BeautifulSoup(scr, "lxml")
    full_text = soup.find("div", {"itemprop": "articleBody", "data-js": "article-body"}).find_all("div",
                                                                                                  "article-body-text")
    for item in full_text:
        full = item.find_all("p")
        for part in full:
            result += part.text.strip()
    return result
