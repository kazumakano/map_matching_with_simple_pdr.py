from itertools import combinations
import numpy as np
import particle_filter.script.parameter as pf_param
from map_matching.script.map import Map as MmMap
from . import parameter as param
from . import utility as util


class Map(MmMap):
    def __init__(self, mac_list: np.ndarray) -> None:
        super().__init__(mac_list)

        self._set_corners()

    def _is_corner(self, node_index: int) -> bool:
        is_corner = False
        for i, j in combinations(self.link_nodes[node_index], 2):
            if i != node_index and j != node_index and util.conv_to_acute_angle(util.calc_angle(self.node_poses[node_index], self.node_poses[i], self.node_poses[j])) > param.MIN_CORNER_ANGLE:
                is_corner = True

        return is_corner

    def _set_corners(self) -> None:
        self.corners = np.empty(0, dtype=np.int16)
        for i in range(len(self.node_poses)):
            if self._is_corner(i):
                self.corners = np.hstack((self.corners, np.int16(i)))
        
        print(f"map.py: {len(self.corners)} corners found")

    def draw_corners(self, is_never_cleared: bool = False) -> None:
        if not param.ENABLE_DRAW_CORNERS:
            raise Warning("map.py: drawing corners is not enabled but draw_corners() was called")

        for i in self.corners:
            self._draw_pos((128, 128, 128), is_never_cleared, self.node_poses[i])

    def draw_pos(self, pos: np.ndarray, is_never_cleared: bool = False) -> None:
        if pf_param.ENABLE_CLEAR:
            self.clear()
        self._draw_pos((0, 255, 0), is_never_cleared, pos)
