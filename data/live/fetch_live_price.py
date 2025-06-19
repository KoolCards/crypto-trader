#!/usr/bin/env python3
"""
Script to fetch Ethereum price data from CoinGecko API
"""

import requests
from typing import Dict, Any
from data.persistence.parquet_dao import ParquetDao
from datetime import date

class LivePriceFetcher:
    def __init__(self):
        self.url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        self.dao = ParquetDao("data/ethereum_price.parquet")

    def _fetch_live_price(self) -> float:
        """
        Fetch Ethereum price in USD from CoinGecko API
        
        Returns:
            Dict containing the API response
        """
        # Make GET request to the API
        response = requests.get(self.url)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        print('Extracted price: ', data['ethereum']['usd'])
        return data['ethereum']['usd']
    
    def _insert_live_price(self, price: float) -> None:
        self.dao.insert_data([(date.today(), price)])

    def fetch_and_insert_live_price(self) -> None:
        price = self._fetch_live_price()
        self._insert_live_price(price)


def main():
    """Main function to execute the script"""
    print("Fetching Ethereum price from CoinGecko API...")

    LivePriceFetcher().fetch_and_insert_live_price()

    



if __name__ == "__main__":
    main() 