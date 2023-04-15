from bs4 import BeautifulSoup

def extract_article_data(article_html):
    soup = BeautifulSoup(article_html, "html.parser")

    title_el = soup.find("h1", class_="content--title")
    if title_el is None:
        return None

    title = title_el.text.strip()

    date_time = soup.find("time")["datetime"]

    summary = soup.find("p", class_="content--summary").text.strip()

    main_content_tags = soup.find("div", class_="content--detail-body").find_all("p", class_=None)
    main_content = "\n".join(tag.text.strip() for tag in main_content_tags)


    img_element = soup.find("img", class_="lazy")
    if img_element is not None:
        img_src = img_element.get("data-src")
        img_alt = img_element.get("alt")
    else:
        img_src = None
        img_alt = None

    detail_more_content_tags = soup.select("div.content--detail-more p, div.content--detail-more .body-title, div.content--detail-more .body-text")

    detail_more_content = "\n".join(tag.text.strip() for tag in detail_more_content_tags)

    article_data = {
        "title": title,
        "date_time": date_time,
        "summary": summary,
        "main_content": main_content,
        "img_src": img_src,
        "img_alt": img_alt,
        "detail_more_content": detail_more_content
    }

    return article_data
