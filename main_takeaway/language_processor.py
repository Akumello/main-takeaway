from bs4 import BeautifulSoup
from urllib.request import urlopen
import nltk
import re
import html
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist


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


def get_takeaway_output(url: str) -> str:
    output: str = ""

    # Get tokenized article without non-alphabet words
    article: str = extract_web(url)
    article_alphabet: str = re.sub("[^a-zA-Z]", " ", article)
    article_word_tokens: list[str] = word_tokenize(article_alphabet, language='english', preserve_line=True)
    article_sentences: list[str] = sent_tokenize(article)

    # Remove stop words
    filtered_words: list = []
    stop_words = set(stopwords.words('english'))
    for word in article_word_tokens:
        if word.lower() not in stop_words:
            filtered_words.append(word)

    # Find frequency count
    article_frequencies = FreqDist()
    for word in filtered_words:
        article_frequencies[word.lower()] += 1

    # Format output
    word_freq_output: str = "10 Most Common Words:\n"
    for common_word in article_frequencies.most_common(10):
        extra_tab: str = "\t\t" if len(common_word[0]) < 7 else "\t"
        word_freq_output += common_word[0] + ":" + extra_tab + str(common_word[1]) + "\n"

    # Output
    output += word_freq_output

    output += " \nSample Sentences:\n"
    # Search each tokenized sentence for each common word
    for common_word in article_frequencies.most_common(10):
        for sentence in article_sentences:
            sample_found: bool = False

            # Search through tokenized sentence
            sentence_tokens: list[str] = word_tokenize(sentence.lower())
            for word in sentence_tokens:
                if common_word[0] == word:
                    extra_tab: str = "\t\t" if len(common_word[0]) < 7 else "\t"
                    output += common_word[0] + ":" + extra_tab + sentence + "\n \n "
                    sample_found = True
                    break

            if sample_found:
                break  # On to the next common word

    return output
