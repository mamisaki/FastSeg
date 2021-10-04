#!/bin/bash

CONDA_DIR=$HOME/anaconda3
FASTSEG_DIR=$HOME/FastSeg

# activate anaconda environment
. $CONDA_DIR/etc/profile.d/conda.sh
conda activate fastsurfer_gpu

# Run fastSeg
$FASTSEG_DIR/fastSeg.py $@
