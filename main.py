import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from stock import StockData

def get_new_browser_window():
    options = Options()
    options.add_argument('user-data-dir=/Users/jackdonofrio/Library/Application Support/Google/Chrome/Profile 1')
    browser = webdriver.Chrome(executable_path='/Users/jackdonofrio/Desktop/trade-bot/chromedriver', chrome_options=options)
    return browser
def close_browser(browser):
    browser.close()

browser = get_new_browser_window()
browser.get('https://www.marketwatch.com/game/pool-to-the-moon-20')

browser.find_element_by_xpath('/html/body/div[5]/div[3]/div[1]/div[1]/div/div[1]/input').send_keys('GME') # input box