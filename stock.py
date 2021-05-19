from yfinance import Ticker

class StockData:
    """ Accesses current values of a stock from its ticker """    
    def __init__(self, ticker):
        self.ticker = ticker
        stock_history = Ticker(ticker).history()
        self.yesterday_closing_price = stock_history.iat[-2, -4]
        self.current_price = stock_history.iat[-1, -4]
        self.delta = self.current_price - self.yesterday_closing_price
        self.percent_change = self.get_day_over_day_percent_change()
    
    def get_day_over_day_percent_change(self):
        """ Calculates the percent change of the stock between yesterday and today """
        return round(100 * (self.delta) / self.yesterday_closing_price, 5)
    
    def get_stock_data(self):
        """ Returns formatted stock data for easy viewing """
        return {
            'ticker' : self.ticker,
            'price' : self.current_price,
            'delta' : self.delta,
            'percent_change' : self.percent_change
        }


if __name__ == '__main__': 
    """ Testing this module """
    print(StockData('GME').get_stock_data())