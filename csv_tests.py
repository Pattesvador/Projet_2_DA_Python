import requests
import csv

# from bs4 import BeautifulSoup
from page import scrap_page

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

response = requests.get(url)
if response.ok:
   try:
      f = open("book_infos.csv", "x", newline='')
      mywriter = csv.writer(f)
      info_page = scrap_page(url)
      for i in info_page:
         mywriter.writerow(info_page.values())
         # f.write(info_page.values())
      # h = response.headers
      # print(h)
      # for i in h:
      # f.write(i + " " + h[i] + " || ")

   except FileExistsError:
      f = open("book_infos.csv", "w", newline="")
      mywriter = csv.writer(f)
      info_page = scrap_page(url)
      for i in info_page:
         mywriter.writerow(info_page.values())
         # f.write(info_page.values())
      # h = response.headers
      # print(h)
      # for i in h:
         # f.write(i + " " + h[i] + " || ")

   finally:
      f.close()