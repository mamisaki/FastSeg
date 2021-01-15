# FastSeg
MRI anatomical image segmentation tool for fMRI data processing using the FastSurfer.

FastSeg is a fast and accurate anatomical image segmentation tool for making the brain and tissue segmentation masks for using in fMRI data processing.

INSTALL:

Clone FastSeg
```
cd ~
git clone https://github.com/mamisaki/FastSeg.git
```

Clone FastSurfer from https://github.com/Deep-MI/FastSurfer
```
cd FastSeg
git clone https://github.com/Deep-MI/FastSurfer.git
```

Create anaconda env for FastSurfer
```
cd FastSurfer
conda env create -f fastsurfer_env_gpu.yml
```

Copy FastSeg/run_fastsurfer.sh to the directory in the PATH.

Edit run_fastsurfer.sh to set 'cmd_dir'
cmd_dir=PATH_TO_FASTSEG_DIR

USAGE:

run_fastsurfer.sh INPUT_FILE [OUTPUT_PREFIX]
