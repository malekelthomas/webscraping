import os, os.path
import errno
import time
import uuid
from bs4 import BeautifulSoup
import requests as req
from requests.sessions import HTTPAdapter
from urllib3.util.retry import Retry
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

def store_shoe(url: str, shoe_name: str, brand: str, site_name:str):
    session = req.Session()
    retry = Retry(connect=3, backoff_factor=2)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    res = session.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    imgs, name = p.save_product_images_sg(soup, shoe_name) #get product images
    sizesPrices = p.save_prices_sg(soup) #get product prices
    releaseDate = p.save_release_date_sg(soup)
    sku = gen_sku(name)
    j = {
        "brand":brand,
        "model":name,
        "sku":sku,
        "photos":imgs,
        "site_size_price": {
            "sites_sizes_prices":{
                site_name:
                    {
                        "sizes_prices":sizesPrices
                        }
                    }
            },
        "release_date": releaseDate
        }
    res = req.post('http://localhost:8080/sneakers/', json=j)
    
def scroll_and_store_sg(driver, site, product_dict, brand):
    """
        Scroll through and get list of products then store.
    """
    final_item = 0
    print(f'traversing {brand} products on {site}\n')
    while True:
        time.sleep(1)
        #get page source pass to beautiful soup
        page_source = driver.page_source
        #get soup
        soup = BeautifulSoup(page_source, "lxml")
        
        #get links
        a_tags = p.get_links_sg(soup)
        
        #add links with names to dict
        for i in a_tags:
            fullName = p.get_product_name_sg(i['aria-label'])
            product_dict[fullName] = [i['href'],brand, site]
        
        #navigate to last item
        last_item = list(product_dict.items())[-1]
        if final_item == 0:
            final_item = last_item
        elif final_item == last_item:
            break
        
        element = driver.find_element_by_xpath(f'//a[@href=\'{last_item[1][0]}\']')
        driver.execute_script("return arguments[0].scrollIntoView(true);", element)
        final_item = last_item
        
        #check if last item has changed

def save_products(product_dict):
    count = 0 
    for shoe, details in product_dict.items():
        time.sleep(2)
        store_shoe(details[0], shoe, details[1], details[2])
        count +=1
        print(f'stored {shoe} count: {count}\n')