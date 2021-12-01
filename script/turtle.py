import copy
from typing import Tuple
import numpy as np
from pdr.script.turtle import Turtle as PdrTurtle
from . import parameter as param

STOP_STATE = 0
STRAIGHT_STATE = 1
TURN_STATE = 2

class Turtle(PdrTurtle):
    def __init__(self, init_pos: np.ndarray, init_heading: np.float16) -> None:
        super().__init__(init_pos, init_heading)

        self.status = STOP_STATE
        self.heading_hist = np.empty(0, dtype=np.float64)
    
    def right(self, angle: np.float64) -> None:
        super().right(angle)

        self.heading_hist = np.hstack((self.heading_hist, self.heading))
        if len(self.heading_hist) == param.MAX_HEADING_HIST_LEN:
            self.heading_hist = np.delete(self.heading_hist, 0)

        if self.heading_hist.var() > 100:
            self.status = TURN_STATE
        else:
            self.status = STRAIGHT_STATE

    def copy(self) -> Tuple[np.ndarray, np.float64]:
        return copy.deepcopy(self.pos), copy.deepcopy(self.heading)
