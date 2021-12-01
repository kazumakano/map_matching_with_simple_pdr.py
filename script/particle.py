import numpy as np
import particle_filter.script.parameter as pf_param
from map_matching.script.particle import Particle as MmParticle
from . import parameter as param
from .map import Map
from particle_filter.script.window import Window
import particle_filter.script.utility as pf_util


class Particle(MmParticle):
    def random_walk(self, vec: np.ndarray, angle: np.float64) -> None:
        self.walk(np.linalg.norm(vec) + np.random.normal(scale=param.STRIDE_SD), angle + np.random.normal(scale=pf_param.DIRECT_SD))

    def set_likelihood(self, map: Map, win: Window, last_pos: np.ndarray, is_on_corner: bool) -> None:
        super().set_likelihood(map, win, last_pos)

        if not pf_param.IS_LOST:
            if is_on_corner:    # if turtle is turning
                max_corner_weight = 0
                for i in map.corners:
                    corner_weight = pf_util.calc_prob_weight(pf_util.calc_dist_by_pos(self.pos, map.node_poses[i]), 0)
                    if corner_weight > max_corner_weight:
                        max_corner_weight = corner_weight

                self.likelihood += max_corner_weight
