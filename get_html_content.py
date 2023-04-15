import requests

def get_html_content(url, headers):
    if not url.startswith("http"):
        url = "https://" + url
    response = requests.get(url, headers=headers)
    return response.content.decode("utf-8")
