import peewee
from jesse.services.db import database


if database.is_closed():
    database.open_connection()


class Account(peewee.Model):
    id = peewee.UUIDField(primary_key=True)
    exchange = peewee.CharField()
    username = peewee.CharField()
    password = peewee.CharField()
    fa_key = peewee.CharField()
    is_active = peewee.BooleanField()
    exchange_token = peewee.CharField()

    class Meta:
        from jesse.services.db import database

        database = database.db

    def __init__(self, attributes: dict = None, **kwargs) -> None:
        peewee.Model.__init__(self, attributes=attributes, **kwargs)

        if attributes is None:
            attributes = {}

        for a, value in attributes.items():
            setattr(self, a, value)


# if database is open, create the table
if database.is_open():
    Account.create_table()
