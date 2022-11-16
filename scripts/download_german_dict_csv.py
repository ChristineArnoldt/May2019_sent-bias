
import requests
URL = "https://raw.githubusercontent.com/jarinox/python-grammar-de/master/data/german.csv"
response = requests.get(URL)
open("data/german.csv", "wb").write(response.content)