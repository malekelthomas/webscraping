import os, os.path
import errno
import time
import uuid
from bs4 import BeautifulSoup
import requests as req
import parsers as p

# Taken from https://stackoverflow.com/a/600612/119527
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')

def safe_open_wb(path): #write bytes
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'wb')

def gen_sku(name):
    skuNum = str(uuid.uuid1()).split("-")
    sku = ""
    splitName = name.split('-')
    for i in range(len(splitName)):
        if splitName[i] != '':
            sku+=splitName[i][0]
    sku+=skuNum[0].upper()
    return sku

def store_shoe(url: str, shoeName: str):
    res = req.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    imgs, name = p.save_product_images_sg(soup, shoeName) #get product images
    sizesPrices = p.save_prices_sg(soup) #get product prices
    releaseDate = p.save_release_date_sg(soup)
    sku = gen_sku(name)
    j = {
        "brand":"Jordan",
        "model":name,
        "sku":sku,
        "photos":imgs,
        "site_size_price": {
            "sites_sizes_prices":{
                "STADIUMGOODS":
                    {
                        "sizes_prices":sizesPrices
                        }
                    }
            },
        "release_date": releaseDate
        }
    res = req.post('http://localhost:8080/sneakers/', json=j)