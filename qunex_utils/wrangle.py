
import os
import glob
import functools
import numpy as np
import qunex from qunex


class qunex(object):
    '''
    Class with functions for wrapping around an individual QUNEX subject directory
    '''
    def __init__(self, dir):
        self.dir = dir  
        self._create_paths()
    
    def _read_session(self):
        # read session metadata file with information about included scans
        with open(self.session_txt, 'r') as f:
            sesh_data = f.readlines()

        sesh_data = [x.replace('\n', '') for x in sesh_data]
        sesh_dict = dict([x.split(': ') for x in sesh_data if ':' in x])
        setattr(self, 'session_info', sesh_dict)

        # figure out which runs are EPI/functiona/bold
        mri_keys  = [x for x in sesh_dict.keys() if '0' in x]
        bold_runs = [sesh_dict[k] for k in mri_keys if 'bold' in sesh_dict[k]]
        bold_dict = dict(zip(range(1,len(bold_runs)+1), bold_runs))
        setattr(self, 'bold_dict', bold_dict)

    def _create_paths(self):
        self.paths = dict()

        # define paths to the following qunex subdirectories
        folders = ['hcp', 'images', 'bids','nii']
        for folder in folders:
            if os.path.exists(os.path.join(self.dir, folder)):
                setattr(self, 'dir_{}'.format(folder), os.path.join(self.dir, folder))

        # there should be a log/txt file with session information
        if os.path.exists(os.path.join(self.dir, 'session.txt')):
            setattr(self, 'session_txt', os.path.join(self.dir, 'session.txt'))
            self._read_session()
            

    def _print(self):
        print(self.dir)


def wrangle(qunex_dirs, out_dir):
    '''
    Perform operations on list of qunex directories
    '''

    def _catch_output(qunex_data):
        motion_list = []
        mask_list = []
        fs_list = []
        for o in qunex_data:
            motion_df, mask_df, fs_df = o
            motion_list.append(motion_df)
            mask_list.append(mask_df)
            fs_list.append(fs_df)
        return_motion_df = pd.concat(motion_list)
        return_mask_df   = pd.concat(mask_list)
        return_fs_df    = pd.concat(fs_list)
        return return_motion_df, return_mask_df, return_fs_df

    # extract data from each QUNEX directory
    qunex_dirs = glob.glob(os.path.join('/fmri-qunex/research/imaging/datasets/embarc/processed_data/pf-pipelines/qunex-nbridge/studies/embarc-20201122-LHzJPHi4/sessions/*'))
    qunex_dirs = [x for x in qunex_dirs if '_' in x]
    out_dir    = '/home/ubuntu/embarc_qunex'

    # reformat motion/freesurfer/mask stats
    qunex_output = list(map(functools.partial(wrangle_run, out_dir=out_dir), qunex_dirs))
    motion_df, mask_df, fs_df = _catch_output(qunex_output)


def wrangle_run(qunex_dir, out_dir):
    '''
    Pull data or perform operations on specific QUNEX run
    '''
    
    qunex_run   = qunex(qunex_dir)
    print('Working on: {}'.format(qunex_run.session_info['id']))
    motion_df   = read_bold_motion(qunex_run)
    mask_df     = read_mask_stats(qunex_run)
    freesurf_df = read_freesurfer(qunex_run, stat_files=['aseg.stats', 'lh.aparc.stats', 'rh.aparc.stats'])

    return motion_df, mask_df, freesurf_df


def read_freesurfer(qunex_run, stat_files=['aseg.stats', 'lh.aparc.stats', 'rh.aparc.stats']):
    '''
    Read freesurfer stats
    '''

    def _lines_to_df(fs_data, qunex_run):
        # read freesurfer data
        hemi = [x.split('hemi')[1].replace('\n','').replace(' ','') for x in fs_data if 'hemi' in x][0]
        fs_hdrs = [x for x in fs_data if 'ColHeaders' in x][0].split()
        fs_hdrs = fs_hdrs[2:]
        fs_df   = pd.DataFrame([x.split() for x in fs_data if '#' not in x])
        fs_df.columns = fs_hdrs
        fs_df.insert(0, 'id', qunex_run.session_info['id'])
        return fs_df

    def _read_surface(fs_data, qunex_run):
        # read freesurfer data
        hemi  = [x.split('hemi')[1].replace('\n','').replace(' ','') for x in fs_data if 'hemi' in x][0]
        fs_df = _lines_to_df(fs_data, qunex_run)

        meas_list = []
        for meas in ['SurfArea', 'ThickAvg', 'GrayVol']:
            fs_wide = fs_df.pivot(columns='StructName', values=meas, index='id')
            fs_wide.columns = meas + '_' + hemi + '_' +  fs_wide.columns
            meas_list.append(fs_wide)
        meas_df = pd.concat(meas_list, 1)
        return meas_df

    def _read_volume(fs_data, qunex_run):
        fs_df = _lines_to_df(fs_data, qunex_run)
        fs_wide = fs_df.pivot(columns='StructName', values='Volume_mm3', index='id')
        return fs_wide

    def _read_hdr(fs_dir, stat_file, qunex_run):
        fs_path = os.path.join(fs_dir, 'stats', stat_file)
        with open(fs_path, 'r') as f:
            fs_data = f.readlines()
        measure_lines = [x for x in fs_data if '# Measure' in x]
        measure_list  = [x.split()[2].replace(',','') for x in measure_lines]
        value_list    = [float(x.split()[-2].replace(',','')) for x in measure_lines]
        aseg_row      = pd.DataFrame(value_list).transpose()
        aseg_row.columns = measure_list
        aseg_row.insert(0, 'id', qunex_run.session_info['id'])
        aseg_row.set_index(['id'], inplace=True)
        return aseg_row


    # path to freesurfer output
    fs_dir       = os.path.join(qunex_run.dir_hcp, qunex_run.session_info['id'], 'T1w', qunex_run.session_info['id'])
    
    # read data stored in the header of stats files
    hdr_measures = _read_hdr(fs_dir, stat_files[0], qunex_run)


    fs_list = []
    fs_list.append(hdr_measures)
    for stat_file in stat_files:
        # read freesurfer data as lines
        fs_path = os.path.join(fs_dir, 'stats', stat_file)
        with open(fs_path, 'r') as f:
            fs_data = f.readlines()

        # pull relevant data
        anat_type = [x.split('anatomy_type')[1].replace('\n','').replace(' ','') for x in fs_data if 'anatomy_type' in x][0]
        if anat_type == 'surface':
            fs_df = _read_surface(fs_data, qunex_run)
        elif anat_type == 'volume':
            fs_df = _read_volume(fs_data, qunex_run)
        
        fs_list.append(fs_df)
    # return combined freesurfer dataframe
    fs_df = pd.concat(fs_list, 1)
    return fs_df


def read_mask_stats(qunex_run):
    '''
    Read stats about mask coverage
    '''

    mask_list = []
    for bold in qunex_run.bold_dict.keys():
        res_dir  = os.path.join(qunex_run.dir_hcp, qunex_run.session_info['id'], 'MNINonLinear/Results', str(bold))
        stats_df = pd.read_csv(os.path.join(res_dir, '{}_finalmask.stats.txt'.format(bold)))
        stats_df.insert(0, 'bold', bold)
        stats_df.insert(0, 'id', qunex_run.session_info['id'])
        mask_list.append(stats_df)

    mask_df = pd.concat(mask_list)
    return mask_df


def read_bold_motion(qunex_run):
    '''
    Read motion estimates from QUNEX formatted bold runs
    '''
    def _read_motion(read_path):
        if os.path.exists(read_path):
            with open(read_path, 'r') as f:
                dat = f.readlines()
            return_dat = float(dat[0].replace('\n',''))
        else: 
            return_dat = np.nan
        return return_dat

    # read the relative/absolute motion for each run
    est_list = []
    for bold in qunex_run.bold_dict.keys():
        bold_dir = os.path.join(qunex_run.dir_hcp, qunex_run.session_info['id'], str(bold))
        for motion_file in ['Movement_AbsoluteRMS_mean.txt', 'Movement_RelativeRMS_mean.txt']:
            est = _read_motion(os.path.join(bold_dir, motion_file))
            est_series = pd.Series({'id': qunex_run.session_info['id'],
                                    'scan': bold, 
                                    'measure': motion_file.replace('.txt',''),
                                    'motion':est})
            est_list.append(est_series)
    motion_df = pd.DataFrame(est_list)
    return motion_df




