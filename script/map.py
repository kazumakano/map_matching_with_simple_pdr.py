from map_matching.script.map import Map as MmMap
import particle_filter.script.parameter as pf_param 
import numpy as np


class Map(MmMap):
    # for PDR
    def draw_pos(self, pos: np.ndarray, is_never_cleared) -> None:
        if pf_param.ENABLE_CLEAR:
            self.clear()
        self._draw_any_pos(pos, (0, 255, 0), is_never_cleared)
