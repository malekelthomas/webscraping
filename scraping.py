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

SITES = ['STOCKX','NIKE','ADIDAS','PUMA','STADIUMGOODS','FLIGHTCLUB']


#chrome driver
driver = webdriver.Chrome()

#go to stadiumgoods
driver.get("http://www.stadiumgoods.com")

#check correct website loaded
assert "Stadium" in driver.title

""" #setup actions
actions = ActionChains(driver)

#get link to jordan page
jordan_link = driver.find_element_by_xpath("/html[@id='top']/body[@class='cms-index-index us-store fndtn']/div[@class='wrapper']/div[@class='page']/header[@id='header']/div[@class='page-header-container']/div[@class='header-row-secondary']/div[@id='header-nav']/nav[@class='nav']/ol[@class='nav-primary']/li[@class='level0 nav-2 parent']/a[@class='level0 has-children']")

#click link
actions.click(jordan_link)
actions.perform()
 """
#get urls
product_dict = {}
""" helpers.scroll_and_store_sg(driver, SITES[4], product_dict, "Jordan") """

""" #get link to nike page
nike_link = driver.find_element_by_xpath("/html[@id='top']/body[@class='cms-index-index us-store fndtn']/div[@class='wrapper']/div[@class='page']/header[@id='header']/div[@class='page-header-container']/div[@class='header-row-secondary']/div[@id='header-nav']/nav[@class='nav']/ol[@class='nav-primary']/li[@class='level0 nav-1 first parent']/a[@class='level0 has-children']") """
adidas_link = driver.find_element_by_xpath("/html[@id='top']/body[@class='cms-index-index us-store fndtn']/div[@class='wrapper']/div[@class='page']/header[@id='header']/div[@class='page-header-container']/div[@class='header-row-secondary']/div[@id='header-nav']/nav[@class='nav']/ol[@class='nav-primary']/li[@class='level0 nav-3 parent']/a[@class='level0 has-children']")

#setup actions
actions = ActionChains(driver)

#click link
actions.click(adidas_link)
actions.perform()

helpers.scroll_and_store_sg(driver, SITES[4], product_dict, "adidas")

helpers.save_products(product_dict)



