#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests as req
import parsers as p
import sys

def main():
    
    url, shoeName = sys.argv[1], sys.argv[2]
    r = req.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
   # savedImgs = p.save_product_images_sg(r, shoeName) #save product images
    p.save_prices_sg(soup)

if __name__ == "__main__":
    main()
