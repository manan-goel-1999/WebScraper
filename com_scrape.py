"""This Module Scrapes amazon.com for bestsellers"""
import requests
from bs4 import BeautifulSoup

NAMES = ["Not Available" for x in range(100)]
BOOKURL = ["Not Available" for x in range(100)]
AUTHORS = ["Not Available" for x in range(100)]
RATINGS = ["Not Available" for x in range(100)]
PRICES = ["Not Available" for x in range(100)]
NOFRATINGS = ["Not Available" for x in range(100)]

BOOKTYPE = []

def scrape():
    """ Scrape Through BestSellers on amazon and give their names, links, prices and ratings"""
    pagenum = 1
    i = 0
    while pagenum <= 5:
        ur_l = "https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_"
        ur_l += str(pagenum) + "?_encoding=UTF8&pg=" + str(pagenum) + "&ajax=1"

        ht_ml = requests.get(ur_l)

        ht_ml = ht_ml.text

        soup = BeautifulSoup(ht_ml, "lxml")
        soup1 = BeautifulSoup(ht_ml, "lxml")

        for children in soup1.find_all('span', {'class' : 'a-size-small a-color-secondary'}):
            if children.text not in BOOKTYPE:
                BOOKTYPE.append(children.text)

        data = soup.find_all('div', {'class' : 'zg_itemWrapper'})

        for children in data:
            child = children.find_all('div', {'class' : 'p13n-sc-truncate p13n-sc-line-clamp-1'})
            for children_data in child:
                NAMES[i] = children_data.text.replace('\n', '').replace('  ', '')
                NAMES[i] = NAMES[i].replace(',', ' ').replace(';', ' ')

            child = children.find_all('a', {'class' : 'a-link-normal a-text-normal'})
            for children_data in child:
                BOOKURL[i] = "https://www.amazon.in" + children_data.get('href')
                BOOKURL[i] = BOOKURL[i].replace(',', '')

            child = children.find_all('div', {'class' : 'a-row a-size-small'})
            for children_data in child:
                if children_data.text not in BOOKTYPE:
                    AUTHORS[i] = children_data.text.replace(',', '')

            child = children.find_all('span', {'class' : 'p13n-sc-price'})
            for children_data in child:
                PRICES[i] = children_data.text[3:].replace(',', '')

            child = children.find_all('a', {'class' : 'a-link-normal'})
            for children_data in child:
                children_data = children_data.get('title')
                if children_data is not None:
                    RATINGS[i] = children_data.replace(',', '')

            child = children.find_all('a', {'class' : 'a-size-small a-link-normal'})
            for children_data in child:
                NOFRATINGS[i] = children_data.text.replace(',', '')

            i += 1

        pagenum += 1
    return i

NUMBER = scrape()

OUTFILE = open("./output/com_book.csv", "w")
OUTFILE.write("Name,URL,Author,Price,Number of Ratings,Average Rating\n")
for j in range(NUMBER):
    OUTFILE.write(str(NAMES[j]) + ',' + str(BOOKURL[j]) + ',' + str(AUTHORS[j]))
    OUTFILE.write(',' + str(PRICES[j]) + ',' + str(NOFRATINGS[j]) + ',' + str(RATINGS[j]) + "\n")
