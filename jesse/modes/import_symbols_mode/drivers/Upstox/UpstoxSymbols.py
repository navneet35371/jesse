# https://assets.upstox.com/market-quote/instruments/exchange/complete.json.gz
import os
import requests
import jesse.helpers as jh
from jesse.models import Symbol
import gzip
import shutil
import json

class UpstoxSymbols(object):
    def __init__(self):
        super().__init__()
        self.endpoint = 'https://assets.upstox.com/market-quote/instruments/exchange/complete.json.gz'
        self.chunk_size = 1024 * 1024


    def fetch_symbols(self, exchange):
        response = requests.request("GET", self.endpoint, stream=True)
        path = f'storage/symbols/'
        # filename should be "optimize-" + current timestamp
        filename = f'symbols.json.gz'

        save_path = os.path.join(path, filename)
        with open(save_path, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                fd.write(chunk)
        
        with gzip.open(save_path, 'rb') as f_in:
            with open(path + 'symbols.json', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        self.read_json_and_save_to_db(path,exchange)

        
    def read_json_and_save_to_db(self, path, exchange):
        symbols = []
        with open(path + 'symbols.json', 'r', encoding="utf-8") as f:
            symbolsJson = json.load(f)
            for symbol in symbolsJson:
                symbol['id'] = jh.generate_unique_id()
                symbol['jesse_exchange'] = exchange
                symbol['tradingsymbol'] = symbol['trading_symbol']
                symbol['instrument_token'] = symbol['instrument_key']
                symbols.append(symbol)
                
        
            Symbol.delete().where(Symbol.jesse_exchange == exchange).execute()
            Symbol.insert_many(symbols).on_conflict_ignore().execute()
