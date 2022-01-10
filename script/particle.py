import numpy as np
import particle_filter.script.parameter as pf_param
from map_matching.script.particle import Particle as MmParticle
from . import parameter as param
from .map import Map
import particle_filter.script.utility as pf_util


class Particle(MmParticle):
    def walk(self, angle: np.float64, vec: np.ndarray) -> None:
        if param.ENABLE_PDR_WALK:
            self._walk(angle + np.random.normal(scale=pf_param.DIRECT_SD), np.linalg.norm(vec) + np.random.normal(scale=param.STRIDE_SD))
        else:
            super().random_walk()

    def set_likelihood(self, is_on_corner: bool, last_pos: np.ndarray, map: Map, strength_weight_list: np.ndarray, subject_dist_list: np.ndarray) -> None:
        super().set_likelihood(last_pos, map, strength_weight_list, subject_dist_list)

        if not pf_param.IS_LOST and param.ENABLE_CORNER_WEIGHT:
            if is_on_corner:    # if turtle is turning
                max_corner_weight = 0
                for i in map.corners:
                    corner_weight = pf_util.calc_prob_weight(pf_util.calc_dist_by_pos(map.node_poses[i], self.pos), 0)
                    if corner_weight > max_corner_weight:
                        max_corner_weight = corner_weight

                self.likelihood += max_corner_weight
