
import os
import glob
import functools
import numpy as np
import pandas as pd
import sys
sys.path.append('/home/ubuntu/Projects/qunex_utils/qunex_utils')
from qunex import qunex 
from utils_read import read_freesurfer, read_mask_stats, read_bold_motion


def wrangle(qunex_dirs, out_dir):
    '''
    Perform operations on list of qunex directories
    '''

    def _make_output_dirs(out_dir):
        out_folders  = ['data', 'viz', 'qc', 'viz/pheno_histograms']
        for o_folder in out_folders:
            out_path = os.path.join(out_dir, o_folder)
            if not os.path.exists(out_path):
                os.mkdir(out_path)
                
    def _catch_output(qunex_output):
        motion_list = []
        mask_list = []
        fs_list = []
        for o in qunex_output:
            motion_df, mask_df, fs_df = o
            motion_list.append(motion_df)
            mask_list.append(mask_df)
            fs_list.append(fs_df)
        return_motion_df = pd.concat(motion_list)
        return_mask_df   = pd.concat(mask_list)
        return_fs_df    = pd.concat(fs_list)
        return return_motion_df, return_mask_df, return_fs_df

    # extract data from each QUNEX directory
    out_dir    = '/home/ubuntu/embarc_qunex'
    qunex_dirs = glob.glob(os.path.join('/fmri-qunex/research/imaging/datasets/embarc/processed_data/pf-pipelines/qunex-nbridge/studies/embarc-20201122-LHzJPHi4/sessions/*'))
    qunex_dirs = [x for x in qunex_dirs if '_' in x.split('/')[-1]]

    # create output directories
    _make_output_dirs(out_dir)

    # wrangle each QUNEX run
    qunex_output = list(map(functools.partial(wrangle_run, out_dir=out_dir), qunex_dirs))
    motion_df, mask_df, fs_df = _catch_output([o for o in qunex_output if o != 'Error'])
    fs_df['id'] = fs_df.index

    # save data
    return_paths = []
    for df, name in ((motion_df, 'bold_motion_estimates'), (mask_df, 'bold_mask_estimates'), (fs_df, 'freesurfer_estimates')):
        return_paths.append(os.path.join(out_dir, 'data/{}.csv'.format(name)))
        df.to_csv(os.path.join(out_dir, 'data/{}.csv'.format(name)), index=None)

    return return_paths[0], return_paths[1], return_paths[2]



def wrangle_run(qunex_dir, out_dir):
    '''
    Pull data or perform operations on specific QUNEX run
    '''
    
    #qunex_dir = '/fmri-qunex/research/imaging/datasets/embarc/processed_data/pf-pipelines/qunex-nbridge/studies/embarc-20201122-LHzJPHi4/sessions/CU0025_wk1'
    qunex_run = qunex(qunex_dir)
    try:
        print('Working on: {}'.format(qunex_run.session_info['id']))
        motion_df   = read_bold_motion(qunex_run)
        mask_df     = read_mask_stats(qunex_run)
        freesurf_df = read_freesurfer(qunex_run, stat_files=['aseg.stats', 'lh.aparc.stats', 'rh.aparc.stats'])

        return motion_df, mask_df, freesurf_df
    except:
        return 'ERROR: {}'.format(qunex_run.session_info['id'])








