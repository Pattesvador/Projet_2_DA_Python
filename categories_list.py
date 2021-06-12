import requests
from bs4 import BeautifulSoup

def gather_categories(url):
    response = requests.get(url)
    if not response:
        print("Nope!")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        # categories = soup.find("div", class_="side_categories").find_all("a")
        categories_url = []
        for x in soup.find("div", class_="side_categories").find_all("a"):
        # for x in categories:
            categories_url.append("https://books.toscrape.com/" + x.get("href"))
        categories_url.pop(0)

    return categories_url


var = "\n".join(gather_categories("https://books.toscrape.com/index.html"))
print(var)

# print(gather_categories("https://books.toscrape.com/index.html"))
# print(type(gather_categories("https://books.toscrape.com/index.html")))