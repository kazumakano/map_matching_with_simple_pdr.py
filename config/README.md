# config

This is directory for config files.
Put your config files here.
You can customize following parameters:
| Key                  | Description                                       | Notes                              | Type          |
| ---                  | ---                                               | ---                                | ---           |
| begin                | begin datetime of RSSI log                        | must be like 'yyyy-mm-dd hh:mm:ss' | `str`         |
| end                  | end datetime of RSSI log                          | must be like 'yyyy-mm-dd hh:mm:ss' | `str`         |
| inertial_log_file    | acceleration and angular velocity log file        |                                    | `str`         |
| rssi_log_file        | RSSI log file                                     |                                    | `str`         |
| init_direct          | initial direction [degree]                        |                                    | `float`       |
| init_direct_sd       | standard deviation of direction at initialization |                                    | `float`       |
| init_pos             | initial position [pixel]                          |                                    | `list[float]` |
| init_pos_sd          | standard deviation of position at initialization  |                                    | `float`       |
| particle_num         | number of particles                               |                                    | `int`         |
|                      |                                                   |                                    |               |
| enable_draw_corners  | draw corners or not                               |                                    | `bool`        |
| min_corner_angle     | minimum angle to recognize as corner [degree]     |                                    | `float`       |
|                      |                                                   |                                    |               |
| enable_corner_weight | weighten around corner when turning or not        |                                    | `bool`        |
| enable_pdr_walk      | change policy of walk from random to PDR or not   |                                    | `bool`        |
| stride_sd            | standard deviation of stride at walk              |                                    | `float`       |
