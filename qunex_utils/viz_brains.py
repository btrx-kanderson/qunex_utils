

import matplotlib.pyplot as plt
from nilearn import plotting
import nibabel as nib
from mriqc.viz.utils import plot_mosaic, plot_segmentation, plot_spikes



in_file = '/fmri-qunex/research/imaging/datasets/embarc/processed_data/pf-pipelines/qunex-nbridge/studies/embarc-20201122-LHzJPHi4/sessions/CU0079_baseline/hcp/CU0079_baseline/MNINonLinear/T1w_restore.nii.gz'
in_contours = '/fmri-qunex/research/imaging/datasets/embarc/processed_data/pf-pipelines/qunex-nbridge/studies/embarc-20201122-LHzJPHi4/sessions/CU0079_baseline/hcp/CU0079_baseline/MNINonLinear/Results/1/1_finalmask.nii.gz'
plot_segmentation(
    in_file,
    in_contours,
    out_file=str(out_file),
    cut_coords=self.inputs.cut_coords,
    display_mode=self.inputs.display_mode,
    levels=self.inputs.levels,
    colors=self.inputs.colors,
    saturate=self.inputs.saturate,
    vmin=vmin,
    vmax=vmax,
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


