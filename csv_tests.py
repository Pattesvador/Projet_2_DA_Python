import requests
import csv

# from bs4 import BeautifulSoup
from page import scrap_page

with open("tests.txt") as document:
    element = document.read()
    print(element)
