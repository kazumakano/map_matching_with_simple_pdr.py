from datetime import datetime, timedelta
from typing import Union
from pdr.script.log import Log
from . import parameter as param


class PdrLog(Log):
    def __init__(self, file: Union[str, None] = None, begin: Union[datetime, None] = None, end: Union[datetime, None] = None, enable_sync: bool = False) -> None:
        if enable_sync:
            if begin is not None:
                begin += timedelta(seconds=param.TS_DIFF)
            if end is not None:
                end += timedelta(seconds=param.TS_DIFF)
            super().__init__(file=file, begin=begin, end=end)
            self._sync()
        else:
            super().__init__(file=file, begin=begin, end=end)

    # synchronize timestamp with RSSI log
    def _sync(self):
        for i in range(len(self.ts)):
            self.ts[i] -= timedelta(seconds=param.TS_DIFF)
