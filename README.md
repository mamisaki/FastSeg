# FastSeg
MRI anatomical image segmentation for fMRI data processing using the FastSurfer.

FastSeg is a fast and accurate anatomical image segmentation tool for making the brain, white matter, and ventricle masks for fMRI data processing.

## INSTALL

1 Clone FastSeg
```
cd ~
git clone https://github.com/mamisaki/FastSeg.git
```

2 Clone FastSurfer from https://github.com/Deep-MI/FastSurfer
```
cd FastSeg
git clone https://github.com/Deep-MI/FastSurfer.git
```

3 Create anaconda env for FastSurfer

You need to install miniconda or anaconda if you do not have conda environment.

https://docs.conda.io/en/latest/miniconda.html
https://www.anaconda.com/products/individual#Downloads

```
cd FastSurfer
conda env create -f fastsurfer_env_gpu.yml
```

4 Copy ~/FastSeg/run_fastSeg.sh to the directory in the PATH (e.g., ~/bin/).

USAGE:

run_fastSeg.sh INPUT_FILE [OUTPUT_PREFIX]
