from bs4 import BeautifulSoup
import requests as req
import helpers as h


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
    
    i = 0
    print("--------------------------Grabbing Images-------------------------------\n")
    for img in imgs:
        try:
            if img.get('alt') != None:
                for name in removedNums:
                    if img.get('alt').index(name) != None:
                        if img['src'] in alreadySaved:
                            continue
                        alreadySaved.append(img['src'])
        except ValueError:
            print("not a product img")
    print('--------------------------FOUND ALL IMAGES-------------------------------\n')
    return alreadySaved

def save_prices_sg(soup: BeautifulSoup):
    """
    Returns dictionary of size keys with price values
    :param soup: BeautifulSoup
    """
    sizes = soup.find_all('span', class_='product-sizes__size')
    sizes.pop(0) #Remove choose your size 
    prices = soup.find_all('span', class_="price")
    sizePriceDict = {}
    for price, size in zip(prices, sizes):
        sizePriceDict[size.contents[0]] = price.contents[0]
        
    return sizePriceDict
    
    
