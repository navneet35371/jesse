
import os
import requests
import csv
import jesse.helpers as jh
from jesse.models.Symbol import Symbol
from jesse.models.Account import Account

class KiteSymbols(object):
    def __init__(self):
        super().__init__()
        self.endpoint = 'https://api.kite.trade/instruments'
        self.chunk_size = 1024 * 1024


    def fetch_symbols(self, exchange):
        account = Account.get(exchange='kite')
        headers = {'Authorization': 'enctoken ' + account.exchange_token}
        response = requests.request("GET", self.endpoint, headers=headers,stream=True)
        path = f'storage/symbols/'
        # filename should be "optimize-" + current timestamp
        filename = f'symbols.csv'

        save_path = os.path.join(path, filename)
        with open(save_path, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                fd.write(chunk)
        
        self.read_csv_and_save_to_db(save_path,exchange)

        
    def read_csv_and_save_to_db(self, save_path, exchange):
        symbols = []
        with open(save_path, 'r', encoding="utf-8") as csvfile:
            symbolsfile = csv.reader(csvfile, delimiter=',')
            next(symbolsfile, None)
            for symbol in symbolsfile:
                symbols.append({
                    'id' : jh.generate_unique_id(),
                    'jesse_exchange': exchange,
                    'instrument_token': symbol[0],
                    'exchange_token': symbol[1],
                    'tradingsymbol': symbol[2],
                    'name': symbol[3],
                    'last_price': symbol[4],
                    'expiry': symbol[5],
                    'strike': symbol[6],
                    'tick_size': symbol[7],
                    'lot_size': symbol[8],
                    'instrument_type': symbol[9],
                    'segment': symbol[10],
                    'exchange': symbol[11],
                })
                
        
            Symbol.delete().where(Symbol.jesse_exchange == exchange).execute()
            Symbol.insert_many(symbols).on_conflict_ignore().execute()
