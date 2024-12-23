import requests
from bs4 import BeautifulSoup

REFER_URL = ["https://www.jwell.com/category/column/trivia/column20180118?srsltid=AfmBOoofo9iFN_uWnxsi0shCqHmOqSynmGXV9pw3eanVlaK2oSJ0Kjie"]

#参考サイトからテキストを取得
html = requests.get(REFER_URL[0])
soup = BeautifulSoup(html.content, "html.parser")
print(soup.text)