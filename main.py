import requests
from bs4 import BeautifulSoup
import csv
import os


def gather_categories(url):
    """Récupère les url de toutes les catégories en utilisant l'url de la home page et en retourne la liste"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    categories = soup.find("div", class_="side_categories").find_all("a")
    categories_url = []
    for i in categories:
        categories_url.append("https://books.toscrape.com/" + i.get("href"))
    categories_url.pop(0)

    return categories_url


def gather_books(url):
    """Récupère les URL de tous les livres pour une catégorie en utilisant gather_categories et en retourne la liste"""
    books_list = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    iterable = soup.find_all("h3")

    for i in iterable:
        part_url = i.find("a").get("href")
        books_list.append("https://books.toscrape.com/catalogue/" + "/".join(part_url.split("/")[3:]))
    if soup.find("li", class_="next"):
        next_page_part_url = soup.find("li", class_="next").find("a").get("href")
        books_list.extend(gather_books("/".join(url.split("/")[:-1]) + "/" + next_page_part_url))

    return books_list


def scrap_page(url):
    """Récupère les informations demandées pour un livre et les retourne dans un dictionnaire"""
    response = requests.get(url)
    response.encoding = "utf-8"

    info_page = {}
    soup = BeautifulSoup(response.text, "html.parser")
    info_page["product_page_url"] = response.url
    info_page["universal_product_code"] = soup.find("th", text="UPC").next_sibling.text
    info_page["title"] = soup.find("div", class_="col-sm-6 product_main").h1.text
    print("Téléchargement du livre ", info_page["title"])
    info_page["price_including_tax"] = soup.find("th", text="Price (incl. tax)").next_sibling.text  # [1:]
    info_page["price_excluding_tax"] = soup.find("th", text="Price (excl. tax)").next_sibling.text  # [1:]
    info_page["number_available"] = soup.find("th", text="Availability").next_sibling.next_sibling.text
    product_description = soup.find(id="product_description")
    if product_description:
        info_page["product_description"] = soup.find(id="product_description").next_sibling.next_sibling.text
    else:
        info_page["product_description"] = "No product description available"
    info_page["category"] = soup.find_all("a")[3].text
    info_page["review_rating"] = soup.find("p", class_="star-rating").attrs["class"][1]
    info_page["image_url"] = "https://books.toscrape.com/" + "/".join(soup.find("img").attrs["src"].split("/")[2:])

    write_csv(info_page['category'], info_page)

    return info_page


def create_csv(url):
    """Crée un fichier CSV avec un en-tête et le retourne"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    file_name = soup.find("div", class_="page-header action").find("h1").text + ".csv"
    with open(os.path.join('data',file_name), "a", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([file_name])

    return file_name


def columns_csv(file):
    """crée les en-tête des colonnes dans un fichier CSV """
    columns = [
        "Product page URL",
        "Universal product code",
        "Title",
        "Price including tax",
        "Price excluding tax",
        "number available",
        "Product description",
        "Category",
        "Review rating",
        "Image URL",
    ]

    with open(os.path.join('data', file), "a", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)

    return file

def write_csv(file, dictionnary):
    """Ecris une ligne dans le fichier CSV en utilisant le dictionnaire retourné par scrap_page"""
    with open(os.path.join('data', (file + ".csv")), "a", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(dictionnary.values())

def get_image(title, img_url, compteur):
    """Télécharge l'image d'un livre"""
    file_name = str(compteur) + "-" + conv_file_name(title)[:171] + ".jpg"
    print("Téléchargement de l'image : ", file_name)
    response = requests.get(img_url)

    with open(os.path.join('images', file_name), "wb") as picture:
        picture.write(response.content)


def conv_file_name(title):
    """Vérifie et ôte si besoin les caractères interdits dans les noms de fichiers windows"""
    forbidden_char = ["/", "\\", ":", "*", "?", "\"", "<", ">", "|"]
    for i in title:
        if i in forbidden_char:
            title = title.replace(i, " ")

    return title


# instructions
try:
    os.mkdir(os.getcwd() + '\\data')
except FileExistsError:
    pass
try:
    os.mkdir(os.getcwd() + '\\images')
except FileExistsError:
    pass

compteur = 1

for category in gather_categories("https://books.toscrape.com"):
    columns_csv(create_csv(category))
    for books in gather_books(category):
        print(category)
        book_infos = scrap_page(books)
        get_image(book_infos['title'], book_infos['image_url'], compteur)
        compteur += 1
