
import os
import matplotlib.pyplot as plt
from nilearn import plotting
import nibabel as nib
from mriqc.viz.utils import plot_mosaic, plot_segmentation, plot_spikes
import sys
sys.path.append('/home/ubuntu/Projects/qunex_utils/qunex_utils')
from qunex import qunex 


def acpc_alignment(qunex_run, out_dir):

    #out_dir = '/home/ubuntu/embarc_qunex'

    nii_robustroi = os.path.join(qunex_run.dir_hcp, qunex_run.session_info['id'], 'T1w', 'ACPCAlignment', 'robustroi.nii.gz')

    os.path.join(qunex_run.dir_hcp, qunex_run.session_info['id'], 'T1w', 'ACPCAlignment',)

    ### RobustROI
    out_robustroi = os.path.join(out_dir, 'viz', 'brains', 'robustroi.svg')
    plot_mosaic(img=nii_robustroi,
                out_file=out_robustroi,
                zmax=20)



def viz_brains(qunex_dirs, out_dir):
    '''
    Key visualizations to assess QA of QUNEX processing stream
    '''

    qunex_dir = '/fmri-qunex/research/imaging/datasets/embarc/processed_data/pf-pipelines/qunex-nbridge/studies/embarc-20201122-LHzJPHi4/sessions/CU0025_wk1'
    qunex_run = qunex(qunex_dir)


in_file = '/fmri-qunex/research/imaging/datasets/embarc/processed_data/pf-pipelines/qunex-nbridge/studies/embarc-20201122-LHzJPHi4/sessions/CU0079_baseline/hcp/CU0079_baseline/MNINonLinear/T1w_restore.nii.gz'
in_contours = '/fmri-qunex/research/imaging/datasets/embarc/processed_data/pf-pipelines/qunex-nbridge/studies/embarc-20201122-LHzJPHi4/sessions/CU0079_baseline/hcp/CU0079_baseline/MNINonLinear/Results/1/1_finalmask.nii.gz'
out_file = '/home/ubuntu/embarc_qc/out.svg'

plot_segmentation(
    in_file,
    in_contours,
    out_file=out_file,
    cut_coords=10,
    display_mode='z',
    levels=[0.5],
    colors='red',
    saturate=False
)


PlotContours(
            display_mode="z",
            levels=[0.5, 1.5, 2.5],
            cut_coords=10,
            colors=["r", "g", "b"],
        )



    mni_anat = '/fmri-qunex/research/imaging/datasets/embarc/processed_data/pf-pipelines/qunex-nbridge/studies/embarc-20201122-LHzJPHi4/sessions/CU0079_baseline/hcp/CU0079_baseline/MNINonLinear/T1w_restore.nii.gz'
    tsnr_file = '/home/ubuntu/embarc_qc/tsnr.nii.gz'
    stddev_file = '/home/ubuntu/embarc_qc/stddev.nii.gz'
    fig = plt.figure(figsize=(10,2))
    epi_anat = plotting.plot_stat_map(stat_map_img=tsnr_file, bg_img=mni_anat, figure=fig, colorbar=False, display_mode='x')


    fig = plt.figure(figsize=(10,2))
    native_epi = '/fmri-qunex/research/imaging/datasets/embarc/processed_data/pf-pipelines/qunex-nbridge/studies/embarc-20201122-LHzJPHi4/sessions/CU0079_baseline/hcp/CU0079_baseline/MNINonLinear/Results/1/1.nii.gz'
    native_mask = '/fmri-qunex/research/imaging/datasets/embarc/processed_data/pf-pipelines/qunex-nbridge/studies/embarc-20201122-LHzJPHi4/sessions/CU0079_baseline/hcp/CU0079_baseline/MNINonLinear/Results/1/1_finalmask.nii.gz'

    mni_img = nib.load('/fmri-qunex/research/imaging/datasets/embarc/processed_data/pf-pipelines/qunex-nbridge/studies/embarc-20201122-LHzJPHi4/sessions/CU0079_baseline/hcp/CU0079_baseline/MNINonLinear/T1w_restore.nii.gz')
    epi_img = nib.load('/fmri-qunex/research/imaging/datasets/embarc/processed_data/pf-pipelines/qunex-nbridge/studies/embarc-20201122-LHzJPHi4/sessions/CU0079_baseline/hcp/CU0079_baseline/MNINonLinear/Results/1/1_SBRef.nii.gz')

    fig = plt.figure( subplot_kw={'projection': '3d'})
    epi_anat = plotting.plot_stat_map(stat_map_img=epi_img, bg_img=mni_img, figure=fig, colorbar=False, display_mode='x')

    display = plotting.plot_carpet(native_epi, native_mask, detrend=False, figure=fig)
    display.show()


