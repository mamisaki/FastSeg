#!/bin/bash

# activate anaconda environment
. ${HOME}/anaconda3/etc/profile.d/conda.sh
conda activate fastsurfer_gpu

# Run fastSeg
cmd_dir=$(cd $(dirname $0); pwd)
if test "$#" -eq 1
then
    $cmd_dir/fastSeg.py $1
else
    $cmd_dir/fastSeg.py $1 -o $2
fi

conda deactivate
