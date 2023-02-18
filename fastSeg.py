#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anatomical image segmentation for real-time fMRI processing using FastSurfer
(https://github.com/Deep-MI/FastSurfer).

@author: mmisaki@laureateinstitute.org
"""


# %% import ===================================================================
import numpy as np
import argparse
from pathlib import Path
import subprocess
import torch
import nibabel as nib

# Debug
if '__file__' not in locals():
    __file__ = 'this.py'

no_cuda = (not torch.cuda.is_available())

aseg_mask_IDs = {'Brain': ['>0'],
                 'GM': ['>0', -2, -7, -41, -46, -192, -251, -252, -253, -254,
                        -255, -4, -5, -14, -15, -31, -43, -44, -63, -72, -77],
                 'WM': [2, 41, 192, 251, 252, 253, 254, 255],
                 'Vent': [4, 43],
                 'Vent_all': [4, 5, 14, 15, 43, 44, 72, 213, 221],
                 'Left-Thalamus-Proper': [10],
                 'Left-Caudate': [11],
                 'Left-Putamen': [12],
                 'Left-Pallidum': [13],
                 'Brain-Stem': [16],
                 'Left-Hippocampus': [17],
                 'Left-Amygdala': [18],
                 'Left-Accumbens-area': [26],
                 'Left-VentralDC': [28],
                 'Right-Thalamus-Proper': [49],
                 'Right-Caudate': [50],
                 'Right-Putamen': [51],
                 'Right-Pallidum': [52],
                 'Right-Hippocampus': [53],
                 'Right-Amygdala': [54],
                 'Right-Accumbens-area': [58],
                 'Right-VentralDC': [60],
                 'ctx-lh-caudalanteriorcingulate': [1002],
                 'ctx-lh-caudalmiddlefrontal': [1003],
                 'ctx-lh-corpuscallosum': [1004],
                 'ctx-lh-cuneus': [1005],
                 'ctx-lh-entorhinal': [1006],
                 'ctx-lh-fusiform': [1007],
                 'ctx-lh-inferiorparietal': [1008],
                 'ctx-lh-inferiortemporal': [1009],
                 'ctx-lh-isthmuscingulate': [1010],
                 'ctx-lh-lateraloccipital': [1011],
                 'ctx-lh-lateralorbitofrontal': [1012],
                 'ctx-lh-lingual': [1013],
                 'ctx-lh-medialorbitofrontal': [1014],
                 'ctx-lh-middletemporal': [1015],
                 'ctx-lh-parahippocampal': [1016],
                 'ctx-lh-paracentral': [1017],
                 'ctx-lh-parsopercularis': [1018],
                 'ctx-lh-parsorbitalis': [1019],
                 'ctx-lh-parstriangularis': [1020],
                 'ctx-lh-pericalcarine': [1021],
                 'ctx-lh-postcentral': [1022],
                 'ctx-lh-posteriorcingulate': [1023],
                 'ctx-lh-precentral': [1024],
                 'ctx-lh-precuneus': [1025],
                 'ctx-lh-rostralanteriorcingulate': [1026],
                 'ctx-lh-rostralmiddlefrontal': [1027],
                 'ctx-lh-superiorfrontal': [1028],
                 'ctx-lh-superiorparietal': [1029],
                 'ctx-lh-superiortemporal': [1030],
                 'ctx-lh-supramarginal': [1031],
                 'ctx-lh-frontalpole': [1032],
                 'ctx-lh-temporalpole': [1033],
                 'ctx-lh-transversetemporal': [1034],
                 'ctx-lh-insula': [1035],
                 'ctx-rh-unknown': [2000],
                 'ctx-rh-bankssts': [2001],
                 'ctx-rh-caudalanteriorcingulate': [2002],
                 'ctx-rh-caudalmiddlefrontal': [2003],
                 'ctx-rh-corpuscallosum': [2004],
                 'ctx-rh-cuneus': [2005],
                 'ctx-rh-entorhinal': [2006],
                 'ctx-rh-fusiform': [2007],
                 'ctx-rh-inferiorparietal': [2008],
                 'ctx-rh-inferiortemporal': [2009],
                 'ctx-rh-isthmuscingulate': [2010],
                 'ctx-rh-lateraloccipital': [2011],
                 'ctx-rh-lateralorbitofrontal': [2012],
                 'ctx-rh-lingual': [2013],
                 'ctx-rh-medialorbitofrontal': [2014],
                 'ctx-rh-middletemporal': [2015],
                 'ctx-rh-parahippocampal': [2016],
                 'ctx-rh-paracentral': [2017],
                 'ctx-rh-parsopercularis': [2018],
                 'ctx-rh-parsorbitalis': [2019],
                 'ctx-rh-parstriangularis': [2020],
                 'ctx-rh-pericalcarine': [2021],
                 'ctx-rh-postcentral': [2022],
                 'ctx-rh-posteriorcingulate': [2023],
                 'ctx-rh-precentral': [2024],
                 'ctx-rh-precuneus': [2025],
                 'ctx-rh-rostralanteriorcingulate': [2026],
                 'ctx-rh-rostralmiddlefrontal': [2027],
                 'ctx-rh-superiorfrontal': [2028],
                 'ctx-rh-superiorparietal': [2029],
                 'ctx-rh-superiortemporal': [2030],
                 'ctx-rh-supramarginal': [2031],
                 'ctx-rh-frontalpole': [2032],
                 'ctx-rh-temporalpole': [2033],
                 'ctx-rh-transversetemporal': [2034],
                 'ctx-rh-insula': [2035]}


# %% prep_files ===============================================================
def prep_files(opts):
    """
    Parameters
    ----------
    opts : argparse,Namespace
        opts.in_f : input file name
        opts.prefix : output prefix

    Returns
    -------
    in_f : Path
        input file path for FastSurferCNN
    prefix : Path
        output file prefix
    """

    # --- Get input file type ---
    in_f = Path(opts.in_f).resolve()
    exts = in_f.suffixes
    if exts[-1] == '.gz':
        ftype = exts[-2]
    else:
        ftype = exts[-1]

    # --- Set prefix ---
    prefix = opts.prefix
    if prefix is None:
        out_d = in_f.absolute().parent
        prefix = out_d / (in_f.name.replace(''.join(exts[-2:]), '')
                          + '_fastSeg')
    else:
        prefix = Path(opts.prefix).absolute()

    # --- Convert BRIK to NIfTI ---
    if ftype in ('.HEAD', '.BRIK'):
        prefix = Path(str(prefix).replace('+orig', '').replace('+tlrc', ''))
        nii_f = prefix.absolute().parent / \
            (in_f.name.replace(''.join(exts), '') + '.nii.gz')
        cmd = f"3dAFNItoNIFTI -overwrite -prefix {nii_f} {in_f}"
        subprocess.check_call(cmd, shell=True, stderr=subprocess.PIPE)
        in_f = nii_f

    return (in_f, prefix)


# %% run_FastSurferCNN ========================================================
def run_FastSurferCNN(eval_cmd, fastsurfer_d, in_f, prefix, batch_size):
    """
    Parameters
    ----------
    eval_cmd : Path
        path to FastSurferCNN eval.py command.
    fastsurfer_d : Path
        path to FastSurfer install directory.
    in_f : Path
        input file.
    prefix : Path
        output prefix.
    batch_size : int
        batch size for inference.

    Returns
    -------
    out_mgz : Path
        FastSurferCNN segmentation .mgz image.
    """

    # Set output filename
    fsSeg_mgz = str(prefix) + '.mgz'

    # Run
    cmd = f"cd {fastsurfer_d} && "
    cmd += f"python {eval_cmd.relative_to(fastsurfer_d)}"
    cmd += f" --in_name {in_f} --out_name {fsSeg_mgz} --simple_run"
    cmd += f" --batch_size {batch_size}"
    if no_cuda:
        cmd += ' --no_cuda'
    subprocess.check_call(cmd, shell=True)

    return fsSeg_mgz


# %% make_seg_images ==========================================================
def make_seg_images(fsSeg_mgz, prefix, segs, aseg_mask_IDs=aseg_mask_IDs):

    aseg_img = nib.load(fsSeg_mgz)
    header = aseg_img.header
    affine = aseg_img.affine
    aseg_V = np.asarray(aseg_img.dataobj)

    out_fs = []
    for seg_name in segs:
        seg_idx = aseg_mask_IDs[seg_name]
        out_f = str(prefix) + f"_{seg_name}.nii.gz"

        seg = np.zeros_like(aseg_V)
        for idx in seg_idx:
            if type(idx) == str:
                seg += eval(f"aseg_V {idx}")
            elif idx < 0:
                seg -= aseg_V == -idx
            else:
                seg += aseg_V == idx

        tmp_f = prefix.parent / f'rm_{seg_name}.nii.gz'
        seg_nii_img = nib.Nifti1Image(seg, affine, header)
        nib.save(seg_nii_img, str(tmp_f))

        cmd = ''
        if seg_name == 'Brain':
            cmd += f"3dmask_tool -overwrite -input {tmp_f}"
            cmd += f" -prefix {tmp_f}"
            cmd += " -frac 1.0 -dilate_inputs 5 -5 -fill_holes &&"

        cmd += f"3dfractionize -overwrite -template {in_f} -input {tmp_f}"
        cmd += f" -prefix {tmp_f} -clip 0.5 &&"

        if seg_name == 'Brain':
            cmd += f"3dcalc -overwrite -prefix {out_f} -a {tmp_f} -b {in_f}"
            cmd += " -expr 'step(a)*b'"
        else:
            cmd += f"3dcalc -overwrite -prefix {out_f} -a {tmp_f}"
            cmd += " -expr 'step(a)'"

        subprocess.check_call(cmd, shell=True)
        if tmp_f.is_file():
            tmp_f.unlink()

        out_fs.append(out_f)

    return out_fs


# %% __main__ =================================================================
if __name__ == "__main__":
    # --- Get options ---
    parser = argparse.ArgumentParser()
    parser.add_argument('in_f', help='input file')
    parser.add_argument('-o', '--out', dest='prefix', help='output prefix')
    parser.add_argument('-s', '--seg', dest='segs', nargs='+',
                        default=['Brain', 'WM', 'Vent'],
                        help='Output segments')
    parser.add_argument('--batch_size', type=int, default=8,
                        help="Batch size for inference. Default: 8")
    parser.add_argument('--fastsurfer_dir', help="FastSurfer directory")
    opts = parser.parse_args()

    # --- Check FastSurfer installation ---
    fastsurfer_dir = opts.fastsurfer_dir
    if fastsurfer_dir is None:
        fastsurfer_dir = Path(__file__).absolute().parent / 'FastSurfer'

    fastsurfer_dir = Path(fastsurfer_dir)
    assert fastsurfer_dir.is_dir(), f"Not found {fastsurfer_dir} directory.\n"

    eval_cmd = fastsurfer_dir / 'FastSurferCNN' / 'eval.py'
    assert eval_cmd.is_file(), f"Not found {eval_cmd}\n"

    # Check segmentation variable
    segs = opts.segs
    for seg in segs:
        assert seg in aseg_mask_IDs.keys(), f"{seg} is not defined.\n"

    # --- Prepare files ---
    in_f, prefix = prep_files(opts)

    # --- Run FastSurferCNN ---
    fsSeg_mgz = run_FastSurferCNN(eval_cmd, fastsurfer_dir, in_f, prefix,
                                  opts.batch_size)

    # --- Get Brain, WM, Vent masks ---
    out_fs = make_seg_images(fsSeg_mgz, prefix, segs, aseg_mask_IDs)

    # --- Clean intermediate files ---
    if Path(opts.in_f).stat().st_ino != Path(in_f).stat().st_ino and \
            in_f.is_file():
        in_f.unlink()

    out_fs_str = '\n  '.join([str(p) for p in out_fs])
    print(f"Output images: \n  {out_fs_str}")
