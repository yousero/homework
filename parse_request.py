import json
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

quotes = []

def parse(soup):
  # text, author, keywords 
  for quote in soup.select('.quote'):
    text = ''
    for t in quote.select('.text'):
      text += t.text.strip().strip('“').strip('”')
    author = quote.select('.author')[0].text
    keywords = quote.select('.keywords')[0]['content'].split(',')
    quotes.append({
      'text': text,
      'author': author,
      'keywords': keywords
    })

url = 'https://quotes.toscrape.com/page/'
page = 1
limit = 20

for p in tqdm(range(page, limit + 1)):
  res = requests.get(url + str(p) + '/')
  if res.status_code == 200:
    soup = BeautifulSoup(res.content, "html.parser")
    parse(soup)
  else:
    break

with open('quotes.json', 'w', encoding='utf-8') as f:
  json.dump(quotes, f)
