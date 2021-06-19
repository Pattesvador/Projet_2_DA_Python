import requests
from bs4 import BeautifulSoup

def gather_categories(url):
    response = requests.get(url)
    if not response:
        print("Nope!")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        # categories = soup.find("div", class_="side_categories").find_all("a")
        categories_list = []
        part_url = "https://books.toscrape.com/"
        for x in soup.find("div", class_="side_categories").find_all("a"):
        # for x in categories:
            categories_list.append("https://books.toscrape.com/" + x.get("href"))
        categories_list.pop(0)

    return categories_list


var = "\n".join(gather_categories("https://books.toscrape.com/index.html"))
print(var)

# print(gather_categories("https://books.toscrape.com/index.html"))
# print(type(gather_categories("https://books.toscrape.com/index.html")))