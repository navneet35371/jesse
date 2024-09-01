import math
import time
from datetime import timedelta
from typing import Dict, List, Any, Union
import csv

import arrow
from jesse.models.Account import Account
import pydash
from timeloop import Timeloop

import jesse.helpers as jh
from jesse.exceptions import CandleNotFoundInExchange
from jesse.models import Candle
from jesse.modes.import_candles_mode.drivers import drivers, driver_names
from jesse.modes.import_candles_mode.drivers.interface import CandleExchange
from jesse.config import config
from jesse.services.failure import register_custom_exception_handler
from jesse.services.redis import is_process_active, sync_publish
from jesse.store import store
from jesse import exceptions
from jesse.services.progressbar import Progressbar
from jesse.enums import exchanges
from jesse.services.kite import *



def run(
        mode: str = 'candles',
        running_via_dashboard: bool = True,
):
    if running_via_dashboard:
        config['app']['trading_mode'] = mode

        # first, create and set session_id
        store.app.set_session_id('test')

        register_custom_exception_handler()

    # open database connection
    from jesse.services.db import database
    database.open_connection()

    if running_via_dashboard:
        # at every second, we check to see if it's time to execute stuff
        status_checker = Timeloop()

        @status_checker.job(interval=timedelta(seconds=1))
        def handle_time():
            if is_process_active('test') is False:
                raise exceptions.Termination

        status_checker.start()

    accounts = Account.select()
    for account in accounts:
        if account.exchange == 'kite' and account.is_active == True:
            enctoken = get_enctoken(account.username, account.password, account.fa_key)
            account.exchange_token = enctoken
            account.save()


                 
