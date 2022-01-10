import os.path as path
from datetime import datetime
from glob import glob
import map_matching.script.parameter as mm_param
import particle_filter.script.parameter as pf_param
import script.parameter as param
from particle_filter.script.log import Log
from script.map import Map


def vis_map() -> None:
    map = Map(Log(datetime(2000, 1, 1), datetime(2000, 1, 1), glob(path.join(pf_param.ROOT_DIR, "log/observed/*.csv"))[0]).mac_list)
    if param.ENABLE_DRAW_CORNERS:
        map.draw_corners()
    if mm_param.ENABLE_DRAW_NODES:
        map.draw_nodes()
    if mm_param.ENABLE_DRAW_LINKS:
        map.draw_links()
    if pf_param.ENABLE_SAVE_IMG:
        map.save_img()

    map.show(0)

if __name__ == "__main__":
    import argparse
    from script.parameter import set_params

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf_file", help="specify config file", metavar="PATH_TO_CONF_FILE")
    parser.add_argument("--corner", action="store_true", help="enable draw corners")
    parser.add_argument("-n", "--node", action="store_true", help="enable draw nodes")
    parser.add_argument("-l", "--link", action="store_true", help="enable draw links")
    parser.add_argument("-s", "--save", action="store_true", help="enable save image")
    args = parser.parse_args()

    if (not args.corner) and (not args.node) and (not args.link):
        raise Warning("visualize_corners.py: set flags in order to visualize")

    set_params(args.conf_file)
    param.ENABLE_DRAW_CORNERS = args.corner
    mm_param.ENABLE_DRAW_NODES = args.node
    mm_param.ENABLE_DRAW_LINKS = args.link
    pf_param.ENABLE_SAVE_IMG = args.save

    vis_map()
