import numpy as np
import particle_filter.script.parameter as pf_param
from map_matching.script.particle import Particle as MmParticle
from . import parameter as param


class Particle(MmParticle):
    def random_walk(self, vec: np.ndarray, angle: np.float64) -> None:
        self.walk(np.linalg.norm(vec) + np.random.normal(scale=param.STRIDE_SD), angle + np.random.normal(scale=pf_param.DIRECT_SD))
