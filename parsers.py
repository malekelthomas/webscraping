from posixpath import join
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal
import datetime


def save_product_images_sg(soup: BeautifulSoup, shoe_name):
    """
    Returns image src urls of a Stadium Goods product
    :param soup: BeautifulSoup
    """
    imgs = soup.find_all('img')
    
    alreadySaved = [] #already saved imgs
    
    #join name by - for saving
    joinedShoeName = ('-').join(shoe_name.split())
    
    #split name and remove numbers so they don't get caught in checking alt tags
    
    splitName = shoe_name.split() #split name provided
    removedNums = [] #list of name with removed numbers
    for el in splitName:
        if el.isnumeric():
            continue
        removedNums.append(el)
    
    print("--------------------------Grabbing Images-------------------------------\n")
    for img in imgs:
        try:
            if img.get('alt') != None:
                for name in removedNums:
                    if img.get('alt').index(name) != None:
                        try:
                            if img['src'] in alreadySaved:
                                continue
                            alreadySaved.append(img['src'])
                        except KeyError:
                            continue
        except ValueError:
            print("not a product img")
    print('--------------------------FOUND ALL IMAGES-------------------------------\n')
    return alreadySaved, joinedShoeName

def save_prices_sg(soup: BeautifulSoup):
    """
    Returns dictionary of size keys with price values for Stadium Goods
    :param soup: BeautifulSoup
    """
    sizes = soup.find_all('span', class_='product-sizes__size')
    sizes.pop(0) #Remove choose your size 
    prices = soup.find_all('span', class_="price")
    sizePriceDict = {}
    for price, size in zip(prices, sizes):
        #parse price
        parsedPrice = Decimal(sub(r'[^\d.]', '', price.contents[0]))
        #convert price to int
        intPrice = int(parsedPrice*100)
        sizePriceDict[size.contents[0]] = intPrice
        
    return sizePriceDict

def save_release_date_sg(soup: BeautifulSoup):
    """
    Returns release date of product
    :param soup: BeautifulSoup
    """
    
    release_date = soup.find_all('td', class_="data")
    for i in release_date:
        try:
            #if exception does not occur this is a date
            date = datetime.datetime.strptime(i.contents[0],"%B %d, %Y").strftime("%m/%d/%Y")
            return date
        except ValueError:
            continue

    
def get_links_sg(soup: BeautifulSoup):
    """
    Gets all the shoe links after clicking the brand in the nav bar
    """
    
    shoe_links = soup.find_all('a', class_="ProductSummary___StyledA-sc-1ykpmp8-1")
    
    return shoe_links

def get_product_name_sg(name: str):
    """
    Remove price from product name
    """
    splitName = name.split(", ")
    fullName = []
    
    for i in splitName:
        if '$' in i:
            continue
        fullName.append(i)
        
    fullName = (' ').join(fullName)
    return fullName