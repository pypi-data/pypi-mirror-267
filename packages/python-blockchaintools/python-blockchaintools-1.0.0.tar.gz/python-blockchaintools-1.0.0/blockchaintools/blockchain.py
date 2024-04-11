import requests


from datetime import datetime
from timetools.timeutil import TimeUtil
from positiontools.positionutil import PositionUtil

class BlockChain:

    @staticmethod
    def testDependency():
        current = datetime.now()
        return TimeUtil.get_start_of_date(current)
    
    @staticmethod
    def testPosition():
        return PositionUtil.is_coordinate_in_china(0, 0)

    @staticmethod
    def get_price():
        url = "https://api.coincap.io/v2/assets/bitcoin/history"
        params = {
            "interval": "d1",
            "start": "1712592000000",
            "end": "1712678399000"
        }
        
        res = requests.get(url, params=params)
        
        data = res.json()
        
        prices = data["data"]
        
        for price in prices:
            time = price["time"]
            price_usd = price["priceUsd"]
            print(f"{time}: {price_usd}")