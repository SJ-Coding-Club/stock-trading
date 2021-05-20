import json

class Database:
    """ Class containing functions for handling position data."""
    @staticmethod
    def get_json():
        return json.load(open('positions.json'))
    @staticmethod
    def get_stock_data(ticker):
        return get_json()['ticker']
    @staticmethod
    def update_stock_data(ticker, share_delta, value):
        data = Database.get_json()
        if ticker in data.keys():
            data[ticker] = {
                "shares" : data[ticker]['shares'] + share_delta,
                "value" : value
            }
        else:
            data[ticker] = {
                "shares" : share_delta,
                "value" : value
            }
        if data[ticker]['shares'] == 0:
            del data[ticker]
        with open('positions.json', 'w') as file:
            json.dump(data, file)