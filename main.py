import os.path as path
from datetime import datetime, timedelta
from typing import Any
import numpy as np
import map_matching.script.parameter as mm_param
import particle_filter.script.parameter as pf_param
from particle_filter.script.truth import Truth
import particle_filter.script.utility as pf_util
import pdr.script.parameter as pdr_param
import script.parameter as param
from particle_filter.script.log import Log as PfLog
from particle_filter.script.resample import resample
from particle_filter.script.window import Window
from pdr.script.direction_estimator import DirectEstimator
from pdr.script.distance_estimator import DistEstimator
from pdr.script.log import Log as PdrLog
from script.map import Map
from script.particle import Particle
from script.turtle import TURN_STATE, Turtle


def _set_main_params(conf: dict[str, Any]):
    global BEGIN, END, INERTIAL_LOG_FILE, RSSI_LOG_FILE, INIT_DIRECT, INIT_DIRECT_SD, INIT_POS, INIT_POS_SD, LOST_TRAJECTORY_POLICY, PARTICLE_NUM, RESULT_DIR_NAME

    BEGIN = datetime.strptime(conf["begin"], "%Y-%m-%d %H:%M:%S")
    END = datetime.strptime(conf["end"], "%Y-%m-%d %H:%M:%S")
    INERTIAL_LOG_FILE = str(conf["inertial_log_file"])
    RSSI_LOG_FILE = str(conf["rssi_log_file"])
    INIT_DIRECT = np.float16(conf["init_direct"])
    INIT_DIRECT_SD = np.float16(conf["init_direct_sd"])
    INIT_POS = np.array(conf["init_pos"], dtype=np.float16)
    INIT_POS_SD = np.float16(conf["init_pos_sd"])
    LOST_TRAJECTORY_POLICY = np.int8(conf["lost_trajectory_policy"])
    PARTICLE_NUM = np.int16(conf["particle_num"])
    RESULT_DIR_NAME = None if conf["result_dir_name"] is None else str(conf["result_dir_name"])

def map_matching_with_pdr(conf: dict[str, Any]):
    inertial_log = PdrLog(BEGIN - timedelta(seconds=pf_param.WIN_STRIDE - pdr_param.WIN_STRIDE), END + timedelta(seconds=1 / pdr_param.FREQ), path.join(pdr_param.ROOT_DIR, "log/", INERTIAL_LOG_FILE))
    director = DirectEstimator(inertial_log.val[:, 3:6], inertial_log.ts)
    distor = DistEstimator(inertial_log.val[:, 0:3], inertial_log.ts)
    rssi_log = PfLog(BEGIN, END, path.join(pf_param.ROOT_DIR, "log/observed/", RSSI_LOG_FILE))
    result_dir = pf_util.make_result_dir(RESULT_DIR_NAME)
    map = Map(rssi_log.mac_list, result_dir)
    if pf_param.TRUTH_LOG_FILE is not None:
        truth = Truth(BEGIN, END, result_dir)
    turtle = Turtle(INIT_POS, INIT_DIRECT)

    if pf_param.ENABLE_DRAW_BEACONS:
        map.draw_beacons(True)
    if param.ENABLE_DRAW_CORNERS:
        map.draw_corners(True)
    if mm_param.ENABLE_DRAW_NODES:
        map.draw_nodes(True)
    if pf_param.ENABLE_SAVE_VIDEO:
        map.init_recorder()

    particles = np.empty(PARTICLE_NUM, dtype=Particle)
    poses = np.empty((PARTICLE_NUM, 2), dtype=np.float16)
    directs = np.empty(PARTICLE_NUM, dtype=np.float16)
    for i in range(PARTICLE_NUM):
        poses[i] = np.random.normal(loc=INIT_POS, scale=INIT_POS_SD, size=2).astype(np.float16)
        directs[i] = np.float16(np.random.normal(loc=INIT_DIRECT, scale=INIT_DIRECT_SD) % 360)
    estim_pos = np.array(INIT_POS, dtype=np.float16)

    pdr_win_len = int(pdr_param.WIN_STRIDE * pdr_param.FREQ)
    i = pdr_win_len - 1
    lost_ts_hist = np.empty(0, dtype=datetime)
    t = BEGIN
    while t <= END:
        print("main.py:", t.time())

        last_turtle_pos, last_turtle_heading = turtle.copy()
        while(i < len(inertial_log.ts) and inertial_log.ts[i] < t + timedelta(seconds=1 / pdr_param.FREQ)):
            speed = pf_util.conv_from_meter_to_pixel(distor.get_win_speed(i, pdr_win_len), map.resolution)
            turtle.forward(speed * pdr_param.WIN_STRIDE)

            angular_vel = director.get_win_angular_vel(i, pdr_win_len)
            turtle.right((angular_vel - director.sign * pdr_param.DRIFT) * pdr_param.WIN_STRIDE)

            # map.draw_pos(turtle.pos, True)
            # map.show()

            i += pdr_win_len

        win = Window(t, rssi_log, map.resolution)
        for j in range(PARTICLE_NUM):
            particles[j] = Particle(map.img, estim_pos, poses[j], directs[j])
            particles[j].walk(turtle.heading - last_turtle_heading, turtle.pos - last_turtle_pos)
            particles[j].set_likelihood(turtle.status == TURN_STATE, estim_pos, map, win.strength_weight_list, win.subject_dist_list)

        poses, directs = resample(particles)

        if LOST_TRAJECTORY_POLICY == 1:
            if not pf_param.IS_LOST:
                estim_pos = pf_util.estim_pos(particles)
                map.draw_particles(estim_pos, particles)
            if pf_param.TRUTH_LOG_FILE is not None:
                map.draw_truth_pos(truth.update_err_hist(t, estim_pos, map.resolution, pf_param.IS_LOST), True)

        elif LOST_TRAJECTORY_POLICY == 2:
            if pf_param.TRUTH_LOG_FILE is not None and pf_param.IS_LOST:
                last_estim_pos = estim_pos
                lost_ts_hist = np.hstack((lost_ts_hist, t))
            elif not pf_param.IS_LOST:
                estim_pos = pf_util.estim_pos(particles)
                map.draw_particles(estim_pos, particles)

                if pf_param.TRUTH_LOG_FILE is not None:
                    lerp_num = len(lost_ts_hist)
                    for j, lt in enumerate(lost_ts_hist):
                        map.draw_truth_pos(truth.update_err_hist(lt, pf_util.get_lerped_pos(estim_pos, last_estim_pos, j, lerp_num), map.resolution, True), True)
                    lost_ts_hist = np.empty(0, dtype=datetime)
                    map.draw_truth_pos(truth.update_err_hist(t, estim_pos, map.resolution, False), True)

        map.show()

        if pf_param.ENABLE_SAVE_VIDEO:
            map.record()

        t += timedelta(seconds=pf_param.WIN_STRIDE)

    print("main.py: reached end of log")
    if pf_param.ENABLE_SAVE_IMG:
        map.save_img()
    if pf_param.ENABLE_SAVE_VIDEO:
        map.save_video()
    if pf_param.ENABLE_WRITE_CONF:
        pf_util.write_conf(conf, result_dir)
    if pf_param.TRUTH_LOG_FILE is not None:
        truth.export_err()
    map.show(0)

if __name__ == "__main__":
    import argparse
    from script.parameter import set_params

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf_file", help="specify config file", metavar="PATH_TO_CONF_FILE")

    conf = set_params(parser.parse_args().conf_file)
    _set_main_params(conf)

    map_matching_with_pdr(conf)
