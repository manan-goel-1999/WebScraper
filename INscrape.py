"""This Module Scrapes amazon.in for bestsellers"""
import os
import requests
from bs4 import BeautifulSoup

NAMES = ["Not Available" for x in range(100)]
BOOKURL = ["Not Available" for x in range(100)]
AUTHORS = ["Not Available" for x in range(100)]
RATINGS = ["Not Available" for x in range(100)]
PRICES = ["Not Available" for x in range(100)]

BOOKTYPE = ['Paperback', 'Hardcover', 'Cards', 'Mass Market Paperback']

os.system("clear")

def scrape():
    """ Scrape Through BestSellers on amazon and give their names, links, prices and ratings"""
    pagenum = 1
    i = 0
    while pagenum <= 5:
        URL = "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_" + str(pagenum)
        URL += "?ie=UTF8&pg=" + str(pagenum) + "&ajax=1"

        HTML = requests.get(URL)

        HTML = HTML.text

        soup = BeautifulSoup(HTML, "lxml")

        data = soup.find_all('div', {'class' : 'zg_itemWrapper'})

        for children in data:
            x = children.find_all('div', {'class' : 'p13n-sc-truncate p13n-sc-line-clamp-1'})
            for z in x:
                NAMES[i] = z.text.replace('\n','').replace('  ','').replace(',', ' ')

            x = children.find_all('a',{'class' : 'a-link-normal a-text-normal'})
            for z in x:
                BOOKURL[i] = "https://www.amazon.in" + z.get('href')

            x = children.find_all('div', {'class' : 'a-row a-size-small'})
            for z in x:
                if z.text not in BOOKTYPE:
                    AUTHORS[i] = z.text

            x = children.find_all('span', {'class' : 'p13n-sc-price'})
            for z in x:
                PRICES[i] = z.text[3:]

            i += 1

        pagenum += 1
    return i

number = scrape()
