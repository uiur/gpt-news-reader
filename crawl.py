import sqlite3
from extract_article_data import extract_article_data
from get_html_content import get_html_content
from scrape_articles import scrape_articles
import requests
import json


def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            date_time TEXT NOT NULL,
            summary TEXT NOT NULL,
            main_content TEXT,
            img_src TEXT,
            img_alt TEXT,
            detail_more_content TEXT
        )
    """)
    connection.commit()


def insert_article(connection, article):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO articles (title, url, date_time, summary, main_content, img_src, img_alt, detail_more_content)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        article.get('title'),
        article.get('url'),
        article.get('date_time'),
        article.get('summary'),
        article.get('main_content'),
        article.get('img_src'),
        article.get('img_alt'),
        article.get('detail_more_content')
    ))
    connection.commit()


def get_latest_articles(connection, limit):
    # Get the latest articles by date_time
    cursor = connection.cursor()
    cursor.execute("SELECT title, summary FROM articles ORDER BY date_time DESC LIMIT ?", (limit,))
    latest_articles = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Return a list of dictionaries containing the title and summary of each article
    return [{"title": title, "summary": summary} for title, summary in latest_articles]

def collect_new_articles():
    """
    Collects all articles from the given URL and any subsequent pages
    Returns a list of article objects
    """

    page = 1
    articles = []

    while True:
        # make request and parse response
        url = 'https://www3.nhk.or.jp/news/json16/new_%03d.json' % page
        response = requests.get(url)
        data = json.loads(response.text)

        # add articles to list
        articles += data['channel']['item']

        # check if there are more pages
        if not data['channel']['hasNext']:
            break

        page += 1

    return articles

def main():
    headers = { 'Accept-Language': 'ja-JP' }
    # Connect to the database
    connection = sqlite3.connect("articles.db")

    # Create the articles table if it doesn't exist
    create_table(connection)

    article_summaries = collect_new_articles()
    for article_summary in article_summaries:
      article_path = article_summary['link']
      article_url = 'https://www3.nhk.or.jp/news/' + article_path
      article_html = get_html_content(article_url, headers)
      article_data = extract_article_data(article_html)
      if article_data:
        print(article_url)
        article_data['url'] = article_url
        insert_article(connection, article_data)

    # latest_articles = get_latest_articles(connection, 3)

    # for article in latest_articles:
    #     print(f"Title: {article['title']}\nSummary: {article['summary']}\n")

    # Close the database connection
    connection.close()


if __name__ == '__main__':
    main()
