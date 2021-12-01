import argparse
from datetime import datetime, timedelta
import numpy as np
import map_matching.script.parameter as mm_param
import particle_filter.script.parameter as pf_param
import particle_filter.script.utility as pf_util
import pdr.script.parameter as pdr_param
from particle_filter.script.log import Log as PfLog
from particle_filter.script.resample import resample
from particle_filter.script.window import Window
from pdr.script.direction_estimator import DirectEstimator
from pdr.script.distance_estimator import DistEstimator
from pdr.script.log import FREQ
from script.map import Map
from script.parameter import set_params
from script.particle import Particle
from script.pdr_log import PdrLog
from script.turtle import TURN_STATE, Turtle


def _set_main_params(conf: dict):
    global BEGIN, END, FILE_RANGE_POLICY, LOG_FILE, PARTICLE_NUM, INIT_POS, INIT_POS_SD, INIT_DIRECT, INIT_DIRECT_SD, ESTIM_POS_POLICY

    BEGIN = datetime.strptime(conf["begin"], "%Y-%m-%d %H:%M:%S")
    END = datetime.strptime(conf["end"], "%Y-%m-%d %H:%M:%S")
    FILE_RANGE_POLICY = np.int8(conf["file_range_policy"])     # 1: set log by file and range
                                                               # 2: set log by file
                                                               # 3: set log by range
    LOG_FILE = str(conf["log_file"])                           # log file name
    PARTICLE_NUM = np.uint16(conf["particle_num"])             # the number of particles
    INIT_POS = np.array(conf["init_pos"], dtype=np.float16)    # initial position [pixel]
    INIT_POS_SD = np.float16(conf["init_pos_sd"])              # standard deviation of position at initialization
    INIT_DIRECT = np.float16(conf["init_direct"])              # initial direction [degree]
    INIT_DIRECT_SD = np.float16(conf["init_direct_sd"])        # standard deviation of direction at initialization
    ESTIM_POS_POLICY = np.int8(conf["estim_pos_policy"])       # 1: position of likeliest particle, 2: center of gravity of perticles

def map_matching_with_pdr():
    rssi_log = PfLog(BEGIN, END)
    if FILE_RANGE_POLICY == 1:
        inertial_log = PdrLog(file=LOG_FILE, begin=BEGIN, end=END)
    elif FILE_RANGE_POLICY == 2:
        inertial_log = PdrLog(file=LOG_FILE)
    elif FILE_RANGE_POLICY == 3:
        inertial_log = PdrLog(begin=BEGIN, end=END)

    map = Map(rssi_log)
    turtle = Turtle(INIT_POS, INIT_DIRECT)
    distor = DistEstimator(inertial_log.ts, inertial_log.val[:, 0:3])
    director = DirectEstimator(inertial_log.ts, inertial_log.val[:, 3:6])

    if pf_param.ENABLE_DRAW_BEACONS:
        map.draw_beacons(True)
    if mm_param.ENABLE_DRAW_NODES:
        map.draw_nodes(True)
    if pf_param.ENABLE_SAVE_VIDEO:
        map.init_recorder()

    particles = np.empty(PARTICLE_NUM, dtype=Particle)
    poses = np.empty((PARTICLE_NUM, 2), dtype=np.float16)    # positions
    directs = np.empty(PARTICLE_NUM, dtype=np.float16)       # directions
    for i in range(PARTICLE_NUM):
        poses[i] = np.random.normal(loc=INIT_POS, scale=INIT_POS_SD, size=2)
        directs[i] = np.random.normal(loc=INIT_DIRECT, scale=INIT_DIRECT_SD) % 360
    estim_pos = np.array(INIT_POS, dtype=np.float16)

    t = BEGIN
    j = int(pdr_param.WIN_SIZE * FREQ - 1)
    while t <= END:
        print("main.py:", t.time())

        last_turtle_pos, last_turtle_heading = turtle.copy()
        while(inertial_log.ts[j] < t + timedelta(seconds=pf_param.WIN_STRIDE)):
            speed = pf_util.conv_from_meter_to_pixel(distor.get_win_speed(j), map.resolution)
            turtle.forward(speed * pdr_param.WIN_SIZE)

            angular_vel = director.get_win_angular_vel(j)
            turtle.right((angular_vel - director.sign * pdr_param.DRIFT) * pdr_param.WIN_SIZE)

            map.draw_pos(turtle.pos, True)
            map.show()

            j += int(pdr_param.WIN_SIZE * FREQ)

        win = Window(rssi_log, map, t)
        for i in range(PARTICLE_NUM):
            particles[i] = Particle(map, poses[i], directs[i], estim_pos)
            particles[i].random_walk(turtle.pos - last_turtle_pos, turtle.heading - last_turtle_heading)
            particles[i].set_likelihood(map, win, estim_pos, turtle.status == TURN_STATE)

        poses, directs = resample(particles)

        if not pf_param.IS_LOST:
            map.draw_particles(particles, estim_pos)
            map.show()
            if ESTIM_POS_POLICY == 1:      # likeliest particle
                estim_pos = pf_util.get_likeliest_particle(particles).pos
            elif ESTIM_POS_POLICY == 2:    # center of gravity
                estim_pos = pf_util.get_center_of_gravity(particles)
        if pf_param.ENABLE_SAVE_VIDEO:
            map.record()

        t += timedelta(seconds=pf_param.WIN_STRIDE)

    print("main.py: reached end of log")
    if pf_param.ENABLE_SAVE_IMG:
        map.save_img()
    if pf_param.ENABLE_SAVE_VIDEO:
        map.save_video()
    map.show(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="specify your config file", metavar="PATH_TO_CONFIG_FILE")

    conf = set_params(parser.parse_args().config)
    _set_main_params(conf)

    map_matching_with_pdr()
