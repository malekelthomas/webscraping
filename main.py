#!/usr/bin/env python3
import requests as req
import parsers as p
import sys

def main():
    
    url, shoeName = sys.argv[1], sys.argv[2]
    r = req.get(url)
    savedImgs = p.save_product_images_sg(r, shoeName) #save product images
    

if __name__ == "__main__":
    main()
