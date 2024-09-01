from pydoc import locate
from jesse.enums import exchanges
from jesse.modes.import_symbols_mode.drivers.Upstox.UpstoxSymbols import UpstoxSymbols
from jesse.modes.import_symbols_mode.drivers.Kite.KiteSymbols import KiteSymbols


drivers = {
    exchanges.KITE_SPOT: KiteSymbols,
    exchanges.UPSTOX_SPOT: UpstoxSymbols,
}


driver_names = list(drivers.keys())
