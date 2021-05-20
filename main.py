from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from stock import StockData
from database import Database

class BotActions:

    @staticmethod
    def open_new_browser_window():
        options = Options()
        options.add_argument('user-data-dir=/Users/jackdonofrio/Library/Application Support/Google/Chrome/Profile 1')
        browser = webdriver.Chrome(executable_path='/Users/jackdonofrio/Desktop/trade-bot/chromedriver', chrome_options=options)
        return browser

    @staticmethod
    def short_stock(browser, ticker, shares):
        try:
            browser.get('https://www.marketwatch.com/game/pool-to-the-moon-20')
            browser.find_element_by_xpath('/html/body/div[5]/div[3]/div[1]/div[1]/div/div[1]/input').send_keys(ticker)
            sleep(3)
            browser.find_element_by_xpath('/html/body/div[5]/div[3]/div[1]/div[1]/div/div[2]/table/tbody/tr[1]/td[4]/button').click()
            sleep(2)
            price_at_trade_time = StockData(ticker).current_price
            browser.find_element_by_xpath('/html/body/div[8]/div/div/div[1]/form/div[1]/ul/li[2]').click()
            browser.find_element_by_xpath('/html/body/div[8]/div/div/div[1]/form/div[2]/div[2]/div[1]/input').send_keys(shares)
            browser.find_element_by_xpath('/html/body/div[8]/div/div/div[1]/form/div[3]/div/button[3]').click()
            browser.close()
            # Update position in database
            Database.update_stock_data(ticker, shares, price_at_trade_time)
            print('Position updated')
            sleep(5)

        except:
            print(f'unable to short {shares} shares of {ticker}')

    @staticmethod
    def cover_stock(browser, ticker, shares):
        try:
            browser.get('https://www.marketwatch.com/game/pool-to-the-moon-20')
            browser.find_element_by_xpath('/html/body/div[5]/div[3]/div[1]/div[1]/div/div[1]/input').send_keys(ticker)
            sleep(3)
            browser.find_element_by_xpath('/html/body/div[5]/div[3]/div[1]/div[1]/div/div[2]/table/tbody/tr[1]/td[4]/button').click()
            sleep(2)
            price_at_trade_time = StockData(ticker).current_price
            browser.find_element_by_xpath('/html/body/div[8]/div/div/div[1]/form/div[1]/ul/li[4]').click()
            browser.find_element_by_xpath('/html/body/div[8]/div/div/div[1]/form/div[2]/div[2]/div[1]/input').send_keys(shares)
            browser.find_element_by_xpath('/html/body/div[8]/div/div/div[1]/form/div[3]/div/button[3]').click()
            browser.close()
            # Update position in database
            Database.update_stock_data(ticker, shares * -1, price_at_trade_time)
            print('Position updated')
            sleep(5)

        except:
            print(f'unable to cover {shares} shares of {ticker}')



def display_portfolio_printout():
    from texttable import Texttable
    data = Database.get_json()
    table = Texttable()

    table.set_cols_align(['c'] * 6)
    table.set_cols_valign(['m'] * 6)
    table.add_rows([["stock", "shorted-at", "current-value", "percent-change", "gain-loss", "shares"]])
    for ticker in data:
        stock_api_data = StockData(ticker)
        current_value = stock_api_data.current_price
        percent_change = f"{round(stock_api_data.percent_change,2)}%"
        purchased_value = data[ticker]['value']
        shares = data[ticker]['shares']
        # also note, since we are only using this bot for shorting stocks, gain and loss are flipped
        table.add_row([ticker,purchased_value, current_value, percent_change, shares * (purchased_value - current_value),shares ])

    print(table.draw())

# display_portfolio_printout()

class BotEngine:
    @staticmethod
    def run():
        while True:
            # Algorithm for covering current stocks:
            data = Database.get_json()
            for ticker in data:
                stock_api_data = StockData(ticker)
                percent_change = (stock_api_data.current_price - data[ticker]['value']) / data[ticker]['value'] * 100
                if percent_change < 20: # cover short if it drops 20%
                    BotActions.cover_stock(BotActions.open_new_browser_window(), ticker, data[ticker]['shares'])
            # Algorithm to discover new stocks:
            stocks_to_check = BotEngine.most_volatile_stocks()
            for ticker in stocks_to_check:
                stock_api_data = StockData(ticker)
                if 200 > stock_api_data.percent_change > 50 and stock_api_data.current_price > 5: # buy if valued over $5 and stock increased 50% 
                    # get $200 worth of stock
                    shares = 200 // stock_api_data.current_price
                    BotActions.cover_stock(BotActions.open_new_browser_window(), ticker, shares)

            sleep(10)
    @staticmethod
    def most_volatile_stocks():
        """
        Need to find an API that can do this because selenium shouldn't be doing this job.
        This function is to find tickers and nothing else because the numerical stock data from 
        tradingview can be unreliable.
        """
        browser = BotActions.open_new_browser_window()
        browser.get('https://www.tradingview.com/markets/stocks-usa/market-movers-most-volatile/')
        browser.find_element_by_xpath('/html/body/div[2]/div[6]/div/div/div/div[3]/div[2]/div[3]/table/thead/tr/th[3]').click()
        sleep(2)
        stocks = [browser.find_element_by_xpath(f"/html/body/div[2]/div[6]/div/div/div/div[3]/div[2]/div[3]/table/tbody/tr[{x}]/td[1]/div/div[2]/a").text for x in range(1,6)]
        browser.close()
        sleep(1)
        return stocks

if __name__ == '__main__':
    BotEngine.run()