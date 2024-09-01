import math
import time
from datetime import timedelta
from typing import Dict, List, Any, Union

import arrow
import pydash
from timeloop import Timeloop

import jesse.helpers as jh
from jesse.exceptions import CandleNotFoundInExchange
from jesse.models import Candle
from jesse.modes.import_symbols_mode.drivers import drivers, driver_names
from jesse.modes.import_candles_mode.drivers.interface import CandleExchange
from jesse.config import config
from jesse.services.failure import register_custom_exception_handler
from jesse.services.redis import sync_publish, process_status
from jesse.store import store
from jesse import exceptions
from jesse.services.progressbar import Progressbar
from jesse.enums import exchanges


def run(
        exchange: str,
        mode: str = 'symbols',
        running_via_dashboard: bool = True,
        show_progressbar: bool = False,
):
    if running_via_dashboard:
        config['app']['trading_mode'] = mode

        # first, create and set session_id
        store.app.set_session_id()

        register_custom_exception_handler()

    # open database connection
    from jesse.services.db import database
    database.open_connection()

    if running_via_dashboard:
        # at every second, we check to see if it's time to execute stuff
        status_checker = Timeloop()

        @status_checker.job(interval=timedelta(seconds=1))
        def handle_time():
            if process_status() != 'started':
                raise exceptions.Termination

        status_checker.start()
    
    try:
        driver = drivers[exchange]()
    except KeyError:
        raise ValueError(f'{exchange} is not a supported exchange. Supported exchanges are: {driver_names}')
    
    print(exchange)
    
    driver.fetch_symbols(exchange)

    

    

