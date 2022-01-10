# config

This is directory for config files.
Put your config files here.
You can customize following parameters:
| Key                  | Description                                     | Notes | Type          |
| ---                  | ---                                             | ---   | ---           |
| enable_draw_corners  | draw corners or not                             |       | `bool`        |
| min_corner_angle     | minimum angle to recognize as turning           |       | `float`       |
|                      |                                                 |       |               |
| enable_corner_weight | weighten around corner when turning or not      |       | `bool`        |
| enable_pdr_walk      | change policy of walk from random to PDR or not |       | `bool`        |
| stride_sd            | standard deviation of stride at walk            |       | `float`       |
|                      |                                                 |       |               |
| max_heading_hist_len | maximum length of history of turtle's heading   |       | `int`         |
