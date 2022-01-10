import os.path as path
from typing import Any, Union
import numpy as np
from map_matching.script.parameter import set_params as set_mm_params
from pdr.script.parameter import set_params as set_pdr_params


def _set_map_params(conf: dict[str, Any]) -> None:
    global MIN_CORNER_ANGLE, ENABLE_DRAW_CORNERS

    MIN_CORNER_ANGLE = np.float16(conf["min_corner_angle"])
    ENABLE_DRAW_CORNERS = bool(conf["enable_draw_corners"])

def _set_particle_params(conf: dict[str, Any]) -> None:
    global ENABLE_PDR_WALK, STRIDE_SD, ENABLE_CORNER_WEIGHT

    ENABLE_PDR_WALK = bool(conf["enable_pdr_walk"])
    STRIDE_SD = np.float16(conf["stride_sd"])
    ENABLE_CORNER_WEIGHT = bool(conf["enable_corner_weight"])

def _set_pdr_log_params(conf: dict[str, Any]) -> None:
    global TS_DIFF

    TS_DIFF = float(conf["ts_diff"])    # time difference of inertial sensor log to RSSI log

def _set_turtle_params(conf: dict[str, Any]) -> None:
    global MAX_HEADING_HIST_LEN

    MAX_HEADING_HIST_LEN = np.uint8(conf["max_turtle_heading_hist_len"])

def set_params(conf_file: Union[str, None] = None) -> dict[str, Any]:
    global ROOT_DIR

    ROOT_DIR = path.join(path.dirname(__file__), "../")       # project root directory

    if conf_file is None:
        conf_file = path.join(ROOT_DIR, "config/default.yaml")    # load default file if not specified

    set_mm_params(conf_file)
    conf = set_pdr_params(conf_file)
    _set_map_params(conf)
    _set_particle_params(conf)
    _set_pdr_log_params(conf)
    _set_turtle_params(conf)

    return conf
