#!/bin/bash

# activate anaconda environment
. $HOME/*conda3/etc/profile.d/conda.sh
conda activate fastsurfer

# Run fastSeg
FASTSEG_DIR=$HOME/FastSeg
$FASTSEG_DIR/fast_seg.py $@
