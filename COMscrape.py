"""This Module Scrapes amazon.in for bestsellers"""
import os
import requests
from bs4 import BeautifulSoup

NAMES = ["Not Available" for x in range(100)]
BOOKURL = ["Not Available" for x in range(100)]
AUTHORS = ["Not Available" for x in range(100)]
RATINGS = ["Not Available" for x in range(100)]
PRICES = ["Not Available" for x in range(100)]
NOFRATINGS = ["Not Available" for x in range(100)]

BOOKTYPE = ['Paperback', 'Hardcover', 'Cards', 'Mass Market Paperback']

os.system("clear")

def scrape():
    """ Scrape Through BestSellers on amazon and give their names, links, prices and ratings"""
    pagenum = 1
    i = 0
    while pagenum <= 5:
        URL = "https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_" + str(pagenum) + "?_encoding=UTF8&pg=" + str(pagenum) + "&ajax=1"

        HTML = requests.get(URL)

        HTML = HTML.text

        soup = BeautifulSoup(HTML, "lxml")

        data = soup.find_all('div', {'class' : 'zg_itemWrapper'})

        for children in data:
            x = children.find_all('div', {'class' : 'p13n-sc-truncate p13n-sc-line-clamp-1'})
            for z in x:
                NAMES[i] = z.text.replace('\n','').replace('  ','').replace(',', ' ').replace(';',' ')

            x = children.find_all('a',{'class' : 'a-link-normal a-text-normal'})
            for z in x:
                BOOKURL[i] = "https://www.amazon.in" + z.get('href')
                BOOKURL[i] = BOOKURL[i].replace(',','')

            x = children.find_all('div', {'class' : 'a-row a-size-small'})
            for z in x:
                if z.text not in BOOKTYPE:
                    AUTHORS[i] = z.text.replace(',','')

            x = children.find_all('span', {'class' : 'p13n-sc-price'})
            for z in x:
                PRICES[i] = z.text[3:].replace(',','')

            x = children.find_all('a', {'class' : 'a-link-normal'})
            for z in x:
                z = z.get('title')
                if z is not None:
                    RATINGS[i] = z.replace(',','')

            x = children.find_all('a', {'class' : 'a-size-small a-link-normal'})
            for z in x:
                NOFRATINGS[i] = z.text.replace(',','')

            i += 1

        pagenum += 1
    return i

number = scrape()

outfile = open("com_book.csv","w")
outfile.write("Name,URL,Author,Price,Number of Ratings,Average Rating\n")
for j in range(number):
    outfile.write(str(NAMES[j]) + ',' + str(BOOKURL[j]) + ',' + str(AUTHORS[j]) + ',' + str(PRICES[j]) + ',' + str(NOFRATINGS[j]) + ',' + str(RATINGS[j]) + "\n")
