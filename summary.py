import sqlite3
from jinja2 import Template
import openai
import re

def recommend_articles(articles):
    template = """
    {%- for id, title, summary, url in articles -%}
    {{ id }}: {{ title }}
    {% endfor %}

    ---
    Interested:
    - International
    - Business

    DO NOT recommend:
    - Sports
    - Entertainment
    - Politics
    - COVID-19
    - Sad news (death, accident, etc.)

    Output format:
    N. id: title - reason

    Recommend the most 3 important articles from the above articles.

    1.
    2.
    3.
    """

    template = Template(template)
    prompt = template.render(articles=articles)

    result = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      temperature=0.2,
      messages=[
            {"role": "system", "content": "You are a professional editor. Your objective is to recommend news articles for your customer."},
            {"role": "user", "content": prompt },
        ]
    )

    output = result['choices'][0]['message']['content']
    pattern = r'^(\d+)\. (\d+): (.*?) - (.*)$'

    recommended_articles = []

    for line in output.strip().split('\n'):
        match = re.match(pattern, line)
        if match:
            article_number = match.group(1)
            article_id = match.group(2)
            article_title = match.group(3)
            article_description = match.group(4)

            recommended_articles.append((article_id, article_title, article_description))

    return recommended_articles


def summarize_article(article):
  template = """
  Title: {{ article.title }}
  Body:
  {{ article.detail_more_content }}

  Summarize main points of the article in 3 bullet points.

  Constraints:
  - Keep the language(日本語)
  """

  template = Template(template)
  prompt = template.render(article=article)

  result = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
          {"role": "user", "content": prompt },
      ]
  )

  output = result['choices'][0]['message']['content']
  return output

# main code
connection = sqlite3.connect("articles.db")

# list latest articles in the database
# I need 10 articles
cursor = connection.cursor()
cursor.execute("SELECT id, title, summary, url FROM articles ORDER BY date_time DESC LIMIT ?", (20,))
latest_articles = cursor.fetchall()

recommended_articles = recommend_articles(latest_articles)

# fetch the recommended articles from the database in one query
ids = [id for id, title, description in recommended_articles]
placeholders = ', '.join('?' for id in ids)
cursor.execute(f"SELECT id, title, summary, url, detail_more_content FROM articles WHERE id IN ({placeholders})", ids)
articles = cursor.fetchall()

# convert the articles to a list of dictionaries
articles = [{"id": id, "title": title, "summary": summary, "url": url, "detail_more_content": detail_more_content} for id, title, summary, url, detail_more_content in articles]

for article in articles:
    summary = summarize_article(article)
    reason = next((description for id, title, description in recommended_articles if int(id) == article['id']), None)
    print(f"Title: {article['title']}\nURL: {article['url']} \nSummary:\n{summary}\nReason: {reason}\n")

