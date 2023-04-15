def remove_tags(soup, tag_name):
    for tag in soup.find_all(tag_name):
        tag.extract()
