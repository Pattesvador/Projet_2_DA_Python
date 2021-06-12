import requests
from bs4 import BeautifulSoup

def gather_categories(url):
    response = requests.get(url)
    if not response:
        print("Nope!")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        # categories = soup.find("div", class_="side_categories").find_all("a")
        categories_infos = []
        part_url = "https://books.toscrape.com/"
        for x in soup.find("div", class_="side_categories").find_all("a"):
        # for x in categories:
            category_infos = {
                "category_url": part_url + x.get("href"),
                "category_title": soup.find("li", class_="active").text,
                "category_csv": category_infos["category_title"] + ".csv"
            }
            categories_infos.append("https://books.toscrape.com/" + x.get("href"))
        categories_infos.pop(0)

    return categories_infos


var = "\n".join(gather_categories("https://books.toscrape.com/index.html"))
print(var)

# print(gather_categories("https://books.toscrape.com/index.html"))
# print(type(gather_categories("https://books.toscrape.com/index.html")))