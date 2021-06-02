from os import system
import time
from bs4 import BeautifulSoup, element
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import parsers
import helpers

#chrome driver
driver = webdriver.Chrome()
driver.get("http://www.stadiumgoods.com")

#check correct website loaded
assert "Stadium" in driver.title

#setup actions
actions = ActionChains(driver)

#get link to jordan page
jordan_link = driver.find_element_by_xpath("/html[@id='top']/body[@class='cms-index-index us-store fndtn']/div[@class='wrapper']/div[@class='page']/header[@id='header']/div[@class='page-header-container']/div[@class='header-row-secondary']/div[@id='header-nav']/nav[@class='nav']/ol[@class='nav-primary']/li[@class='level0 nav-2 parent']/a[@class='level0 has-children']")

#click link
actions.click(jordan_link)
actions.perform()

best_seller_hrefs = {}
final_item = 0
#get urls
while True:
    time.sleep(1)
    #get page source pass to beautiful soup
    page_source = driver.page_source
    #get soup
    soup = BeautifulSoup(page_source, "lxml")
    
    #get links
    jordan_a_tags = parsers.get_links_sg(soup)
    
    #add links with names to dict
    for i in jordan_a_tags:
        fullName = parsers.get_product_name_sg(i['aria-label'])
        best_seller_hrefs[fullName] = i['href']
    
    #navigate to last item
    last_item = list(best_seller_hrefs.items())[-1]
    if final_item == 0:
        final_item = last_item
    elif final_item == last_item:
        break
    
    element = driver.find_element_by_xpath(f'//a[@href=\'{last_item[1]}\']')
    driver.execute_script("return arguments[0].scrollIntoView(true);", element)
    final_item = last_item
    
    #check if last item has changed

for shoe, url in best_seller_hrefs.items():
    helpers.store_shoe(url, shoe)
    print(f'stored {shoe}\n')
