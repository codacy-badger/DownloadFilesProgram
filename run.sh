#!/bin/bash

# init
data=$(cd ~/Downloads && pwd)

# run
run_cmd="python main.py -l 2018/08/13"

docker run -it --rm \
    -v="/${PWD}:/work" \
    -v="${data}:/data" \
    -w="/work/src" \
    denden047/scraping \
    ${run_cmd}
