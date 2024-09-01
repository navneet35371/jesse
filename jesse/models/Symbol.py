# instrument_token, exchange_token, tradingsymbol, name, 
# last_price, expiry, strike, tick_size, lot_size, instrument_type, 
# segment, exchange

import peewee
from jesse.services.db import database


if database.is_closed():
    database.open_connection()


class Symbol(peewee.Model):
    id = peewee.UUIDField(primary_key=True)
    jesse_exchange = peewee.CharField(null=True)
    instrument_token = peewee.CharField(null=True)
    exchange_token = peewee.CharField(null=True)
    tradingsymbol = peewee.CharField(null=True)
    name = peewee.CharField(null=True)
    last_price = peewee.FloatField(null=True)
    expiry = peewee.CharField(null=True)
    strike = peewee.FloatField(null=True)
    tick_size = peewee.FloatField(null=True)
    lot_size = peewee.IntegerField(null=True)
    instrument_type = peewee.CharField(null=True)
    segment = peewee.CharField(null=True)
    exchange = peewee.CharField(null=True)
    isin =  peewee.CharField(null=True)
    instrument_key = peewee.CharField(null=True)
    freeze_quantity = peewee.FloatField(null=True)
    trading_symbol = peewee.CharField(null=True)
    short_name = peewee.CharField(null=True)
    security_type = peewee.CharField(null=True)
    weekly = peewee.CharField(null=True)
    expiry = peewee.CharField(null=True)
    underlying_symbol = peewee.CharField(null=True)
    minimum_lot = peewee.FloatField(null=True)
    underlying_key = peewee.CharField(null=True)
    underlying_type = peewee.CharField(null=True)
    strike_price = peewee.FloatField(null=True)
    asset_symbol = peewee.CharField(null=True)
    asset_key = peewee.CharField(null=True)
    asset_type = peewee.CharField(null=True)
    


    class Meta:
        from jesse.services.db import database

        database = database.db
        indexes = ((('tradingsymbol', 'name', 'instrument_token'), True),)

    def __init__(self, attributes: dict = None, **kwargs) -> None:
        peewee.Model.__init__(self, attributes=attributes, **kwargs)

        if attributes is None:
            attributes = {}

        for a, value in attributes.items():
            setattr(self, a, value)

# if database is open, create the table
if database.is_open():
    Symbol.create_table()

