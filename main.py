#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests as req
import parsers as p
import sys
import uuid
import json


def gen_sku(name):
    skuNum = str(uuid.uuid1()).split("-")
    sku = ""
    splitName = name.split('-')
    for i in range(len(splitName)):
        sku+=splitName[i][0]
    sku+=skuNum[0].upper()
    return sku

def main():
    
    url, shoeName = sys.argv[1], sys.argv[2]
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

if __name__ == "__main__":
    main()
