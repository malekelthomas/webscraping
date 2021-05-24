#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests as req
import parsers as p
import sys

def main():
    
    url, shoeName = sys.argv[1], sys.argv[2]
    res = req.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    imgs = p.save_product_images_sg(soup, shoeName) #get product images
    sizesPrices = p.save_prices_sg(soup) #get product prices

if __name__ == "__main__":
    main()
