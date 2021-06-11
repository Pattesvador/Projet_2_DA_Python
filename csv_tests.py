import requests
import csv

# from bs4 import BeautifulSoup
# from page import scrap_page

with open("tests.csv", "a", newline='') as file:
    writer = csv.writer(file)
    writer.writerow((1, 2, 3, 4, 5))
    writer.writerow((1, 2, 3, 4, 5))

