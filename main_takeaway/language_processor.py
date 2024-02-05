from bs4 import BeautifulSoup
from urllib.request import urlopen


def extract_web(url: str) -> str:
    article_html: str = urlopen(url).read()
    soup: BeautifulSoup = BeautifulSoup(article_html, features="html.parser")

    # remove each listed html element
    for tag in soup(["script", "style", "a", "svg", "header", "footer", "head", "noscript", "meta", "link"]):
        tag.extract()  # remove html element tag

    # Extract text within the remaining html tags
    text: str = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = ' '.join(chunk for chunk in chunks if chunk)

    return text
