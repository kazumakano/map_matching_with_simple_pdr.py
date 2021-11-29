import os.path as path
from typing import Union
import numpy as np
from map_matching.script.parameter import set_params as set_mm_params
from pdr.script.parameter import set_params as set_pdr_params


def _set_pdr_log_params(conf: dict) -> None:
    global TS_DIFF

    TS_DIFF = float(conf["ts_diff"])    # time difference of inertial sensor log to RSSI log

def _set_particle_params(conf: dict) -> None:
    global STRIDE_SD

    STRIDE_SD = np.float16(conf["stride_sd"])

def set_params(conf_file: Union[str, None] = None) -> dict:
    global ROOT_DIR

    ROOT_DIR = path.join(path.dirname(__file__), "../")       # project root directory

    if conf_file is None:
        conf_file = path.join(ROOT_DIR, "config/default.yaml")    # load default file if not specified

    set_mm_params(conf_file)
    conf = set_pdr_params(conf_file)
    _set_pdr_log_params(conf)
    _set_particle_params(conf)

    return conf
