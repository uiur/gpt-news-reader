from bs4 import BeautifulSoup, Comment
from extract_article_data import extract_article_data
from get_html_content import get_html_content
from remove_tags import remove_tags

def scrape_articles(url, headers):
    html_content = get_html_content(url, headers)
    soup = BeautifulSoup(html_content, "html.parser")
    remove_tags(soup, "script")
    remove_tags(soup, lambda tag: isinstance(tag, Comment))

    articles = []
    for li in soup.find_all('li'):
        article = {}

        title_element = li.find('em', class_='title')
        if title_element:
            article['title'] = title_element.text.strip()

        time_element = li.find('time')
        if time_element:
            article['datetime'] = time_element['datetime']

        link_element = li.find('a')
        if link_element:
            article_url = 'https://www3.nhk.or.jp' + link_element['href']
            article['url'] = article_url

            article_html = get_html_content(article_url, headers)
            article_data = extract_article_data(article_html)
            article.update(article_data)

            articles.append(article)

    return articles
