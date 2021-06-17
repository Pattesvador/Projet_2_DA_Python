import requests
import csv

# from bs4 import BeautifulSoup
# from page import scrap_page

dico = {"valeur 1": 1, "valeur 2": 2, "valeur 3": 3}
with open("tests.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(dico.values())
    # writer.writerow(["12345"])

