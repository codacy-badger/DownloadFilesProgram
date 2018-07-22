#!/bin/bash

# run
run_cmd="python main.py"
run_cmd="touch test.txt"

docker run -it --rm \
    -v="/${PWD}:/work" \
    -v="${data}:/data" \
    -w="/work/src" \
    denden047/scraping \
    ${run_cmd}
