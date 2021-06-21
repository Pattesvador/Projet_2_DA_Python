import requests
from bs4 import BeautifulSoup
import csv
import os


def gather_books(url, books_list):
    response = requests.get(url)
    # books_list = []
    if not response:
        print("Nope!")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        header_title = soup.find("li", class_="active").text
        datas_file_path = os.path.join('data', header_title + ".csv")
        iterable = soup.find_all("h3")
        for i in iterable:
            part_url = i.find("a").get("href")
            books_list.append(construct_url("https://books.toscrape.com/catalogue/", part_url))
        if soup.find("li", class_="next"):
            # print(soup.find("li", class_="next").find("a").get('href'))
            next_page_part_url = soup.find("li", class_="next").find("a").get("href")
            gather_books(construct_url_2(response.url, next_page_part_url), books_list)

        with open(datas_file_path, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([header_title])
            writer.writerow([
                "Product page URL",
                "Universal product code",
                "Title", "Price including tax",
                "Price excluding tax", "Number available",
                "Product description",
                "Category",
                "Review rating",
                "Image URL"
            ])

        return books_list, datas_file_path


def construct_url(url, part_url):
    part_url = part_url.split("/")
    part_url = list(dict.fromkeys(part_url))
    part_url.pop(0)
    part_url = "/".join(part_url)
    url = url + part_url

    return url


def construct_url_2(url, part_url):
    url = url.split("/")
    url.pop(-1)
    url.append(part_url)
    url = "/".join(url)

    return url


# var = "\n".join(gather_books("https://books.toscrape.com/catalogue/category/books/travel_2/index.html"))
# print(var)
# print(len(gather_books("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")))
var = "\n".join(gather_books("https://books.toscrape.com/catalogue/category/books/mystery_3/index.html", books_list=[])[0])
print(var, len(gather_books("https://books.toscrape.com/catalogue/category/books/mystery_3/index.html", books_list=[])[0]))
# var = "\n".join(gather_books("https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html", books_list = []))
# print(var)