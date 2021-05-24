from bs4 import BeautifulSoup
import requests as req
import helpers as h


def save_product_images_sg(response, shoe_name):
    """
    Stores and returns image src urls of a Stadium Goods product
    """
    html_content = response.content
    soup = BeautifulSoup(html_content, 'lxml')
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
                        r = req.get(img['src'])
                        try:
                            with h.safe_open_wb('imgs/'+joinedShoeName+'/'+joinedShoeName+'-'+str(i)+'.png') as f:
                                f.write(r.content)
                                f.close()
                            i += 1
                        except req.exceptions.MissingSchema:
                            print("invalid url")
        except ValueError:
            print("not a product img")
    print('--------------------------FOUND ALL IMAGES-------------------------------\n')
    return alreadySaved

def save_prices_sg(response):
    """
    Grabs prices of a Stadium Goods product
    """
    
    html_content = response.content
    soup = BeautifulSoup(html_content, 'lxml')
    prices = soup.find_all('span', class_="price")
    for price in prices:
        print(price.contents)
    
    
