import particle_filter.script.parameter as pf_param
import map_matching.script.parameter as mm_param
import script.parameter as param
from script.map import Map
from particle_filter.script.log import Log
from datetime import datetime

def vis_map() -> None:
    map = Map(Log(datetime(2000, 1, 1), datetime(2000, 1, 1)))    # whenever is fine
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
    parser.add_argument("-c", "--config", help="specify your config file", metavar="PATH_TO_CONFIG_FILE")
    parser.add_argument("--corner", action="store_true", help="enable draw corners")
    parser.add_argument("-n", "--node", action="store_true", help="enable draw nodes")
    parser.add_argument("-l", "--link", action="store_true", help="enable draw links")
    parser.add_argument("-s", "--save", action="store_true", help="enable save image")
    args = parser.parse_args()

    if (not args.corner) and (not args.node) and (not args.link):
        raise Warning("visualize_nodes_and_links.py: set flags in order to visualize")

    set_params(args.config)
    param.ENABLE_DRAW_CORNERS = args.corner
    mm_param.ENABLE_DRAW_NODES = args.node
    mm_param.ENABLE_DRAW_LINKS = args.link
    pf_param.ENABLE_SAVE_IMG = args.save

    vis_map()
