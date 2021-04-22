#!/bin/bash

CONDA_DIR=$HOME/anaconda3
FASTSEG_DIR=$HOME/FastSeg

# activate anaconda environment
. $CONDA_DIR/etc/profile.d/conda.sh
conda activate fastsurfer_gpu

# Run fastSeg
# cmd_dir=$FASTSEG_PATH
#cmd_dir=$(cd $(dirname $0); pwd)  # The same directory as this file
if [ "$#" -eq 1 ]; then
    $FASTSEG_DIR/fastSeg.py $1
elif [ "$#" -eq 2 ]; then
    $FASTSEG_DIR/fastSeg.py $1 -o $2
elif [ "$#" -eq 3 ]; then
    $FASTSEG_DIR/fastSeg.py $1 -o $2 --batch_size $3
else
    echo "usage: run_fastSeg.py input_file [OUTPUT_PREFIX] [BATCH_SIZE]"
fi
