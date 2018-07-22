#!/bin/bash

# init
data=$(cd ~/Downloads && pwd)

# run
run_cmd="python main.py"

docker run -it --rm \
    -v="/${PWD}:/work" \
    -v="${data}:/data" \
    -w="/work/src" \
    denden047/scraping \
    ${run_cmd}
