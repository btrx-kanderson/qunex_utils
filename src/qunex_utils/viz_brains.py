
import os
import cairosvg
import numpy as np
import matplotlib.pyplot as plt
from nilearn import plotting
import nibabel as nib
from mriqc.viz.utils import plot_mosaic, plot_segmentation, plot_spikes
import sys
sys.path.append('/home/ubuntu/Projects/qunex_utils/qunex_utils')
from qunex import qunex 


def create_odir(out_dir, id):
    '''
    Create individual output directory for brain visualizations 

    out_dir
        |-- viz
            |-- brains
                |-- subj001
                    |-- reports
                    |-- anat
                        |-- ACPC
                        |-- BrainExtraction
                        |-- RobustROI
                    |-- func
    '''
    # brain visualization directory
    anat_dir = os.path.join(out_dir, 'viz', 'brains', id, 'anat')
    # diff output folders for anat and func
    for f in ['anat', 'func', 'report']:
        cur_dir = os.path.join(out_dir, 'viz', 'brains', id, f)
        if not os.path.exists(cur_dir):
            os.makedirs(cur_dir)
    # anatomical subdirectories
    for f in ['ACPC', 'BrainExtraction', 'RobustROI']:
        cur_dir = os.path.join(out_dir, 'viz', 'brains', id, 'anat', f)
        if not os.path.exists(cur_dir):
            os.makedirs(cur_dir)
    



def plot_anat_w_olay(anat, olay=None, display_mode='z', save_png=None, threshold=None, cut_coord=None):
    '''
    '''

    if display_mode == 'mosaic' and cut_coord == None:
        display = plotting.plot_anat(anat_img=anat, 
                                    display_mode=display_mode, 
                                    cut_coord=cut_coord, 
                                    threshold=threshold, 
                                    draw_cross=False)
    else:   
        display = plotting.plot_anat(anat_img=anat, 
                                    display_mode=display_mode, 
                                    threshold=threshold, 
                                    draw_cross=False)
    if olay != None: 
        display.add_contours(img=olay)
    print('Saving Figure: {}'.format(save_png))
    display.savefig(save_png)



def anat_qc_images(qunex_run, out_dir):
    '''
    Produce png/svg visualizations of key anatomical volumes

    (1) Robust ROI
    (2) ACPC T1w to MNI152
    (3) Brain Extraction Mask
    '''

    # individual specific output directory for storing pngs
    anat_basedir = os.path.join(out_dir, 'viz/brains', qunex_run.session_info['id'], 'anat')

    # list of tuples used for generating a final html report
    html_list = []


    ### -----------
    ### (1) RobustROI
    ### -----------
    print('Making PNGs to check robustroi.nii.gz')
    # input nifti
    nii_robustroi = os.path.join(qunex_run.dir_hcp, qunex_run.session_info['id'], 'T1w', 'ACPCAlignment', 'robustroi.nii.gz')
    
    # vis outputs
    out_robustroi_svg = os.path.join(anat_basedir, 'RobustROI', 'robust_roi.svg')
    out_robustroi_png = os.path.join(anat_basedir, 'RobustROI', 'robust_roi.png')

    # simple plot to check whether brain matter is cutoff
    plot_mosaic(img=nii_robustroi,
                out_file=out_robustroi_svg,
                zmax=20)
    # convert svg to png
    cairosvg.svg2png(url=out_robustroi_svg, write_to=out_robustroi_png)
    
    # add description and filepath
    relative_path = '../anat/{}'.format(out_robustroi_png.split('/anat/')[-1])
    html_list.append(('Check that brain tissue is not cut off (Cerebellar cut-off is OK)', [relative_path]))



    ### -----------
    ### (2) ACPC alignment of T1w to MNI template
    ### -----------
    template    = '/home/ubuntu/Projects/qunex_utils/templates/MNI152_T1_0.7mm.nii.gz'
    acpc_final  = os.path.join(qunex_run.dir_hcp, qunex_run.session_info['id'], 'T1w', 'ACPCAlignment', 'acpc_final.nii.gz')
    t1w_acpc    = os.path.join(qunex_run.dir_hcp, qunex_run.session_info['id'], 'T1w', 'T1w_acpc.nii.gz')
    
    # visualize in all three orientations
    acpc_list = []
    t1w_list  = []
    for orient in ['x','y','z']:
        # ACPC-to-MNI
        save_png = os.path.join(out_dir, 'viz/brains', qunex_run.session_info['id'], 'anat/ACPC', 'ACPCcheck_MNI152_to_ACPCfinal_{}.png'.format(orient))
        plot_anat_w_olay(anat=template, olay=acpc_final, display_mode=orient, save_png=save_png)
        acpc_list.append('../anat/{}'.format(save_png.split('/anat/')[-1]))


        # T1w-to-MNI
        save_png = os.path.join(out_dir, 'viz/brains', qunex_run.session_info['id'], 'anat/ACPC', 'ACPCcheck_MNI152_T1w_acpc_{}.png'.format(orient))
        plot_anat_w_olay(anat=template, olay=t1w_acpc, display_mode=orient, save_png=save_png)
        t1w_list.append('../anat/{}'.format(save_png.split('/anat/')[-1]))

    html_list.append(('Check ACPC alignment of acpc_final.nii.gz to MNI152', acpc_list))
    html_list.append(('Check ACPC alignment of T1w_acpc.nii.gz to MNI152', t1w_list))


    ### -----------
    ### (3) Check Brain extraction
    ### -----------
    t1w_acpc_bmask = os.path.join(qunex_run.dir_hcp, qunex_run.session_info['id'], 'T1w', 'T1w_acpc_brain_mask.nii.gz')
    save_png       = os.path.join(out_dir, 'viz/brains', qunex_run.session_info['id'], 'anat/ACPC', 'check_brain_mask.png')
    plot_anat_w_olay(anat=t1w_acpc, olay=t1w_acpc_bmask, display_mode='z', save_png=save_png)
    relative_path  = '../anat/{}'.format(save_png.split('/anat/')[-1])
    html_list.append(('Check Brain Extraction', [relative_path]))




def create_html():
    '''
    Create an html report
    '''

    html = ""
    html_out  = '/home/ubuntu/embarc_qunex/viz/brains/CU0025_wk1/report/mri_anatomical.html'
    html_path = ['./anat/ACPC/check_brain_mask.png', './anat/ACPC/check_brain_mask.png']
    for html_iter in html_list:
        title, img_list = html_iter
        print(title)
        print(img_list)
        html += f"<center><h2>{title}</h2><br>"
        for file in img_list:
            html += f"<center><img src='{file}'/ width=1200></center><br>"

    with open(html_out, "w") as outputfile:
        outputfile.write(html)





def make_func_qc_images(qunex_run, out_dir):
    '''
    '''
    
    run_num = 1

    # individual specific output directory for storing functional pngs
    func_pngdir = os.path.join(out_dir, 'viz/brains', qunex_run.session_info['id'], 'func')
    
    # list of tuples used for generating a final html report
    html_list = []


    ### -----------
    ### check alignment of EPI to T1w
    ### -----------
    t1w_base   = os.path.join(qunex_run.dir_hcp, qunex_run.session_info['id'], 'T1w', 'T1w_acpc_dc_restore.nii.gz')
    scout_over = os.path.join(qunex_run.dir_hcp, qunex_run.session_info['id'], str(run_num), 'Scout2T1w.nii.gz')
    t1w_mepi   = os.path.join(qunex_run.dir_hcp, qunex_run.session_info['id'], str(run_num), 'T1wMulEPI.nii.gz')

    # visualize in all three orientations
    t1wScout_list = []
    t1mulEpi_list = []
    for orient in ['x','y','z']:
        # Scout EPI to T1w
        save_png = os.path.join(func_pngdir, '{}_checkScout2T1w_{}.png'.format(run_num, orient))        
        plot_anat_w_olay(anat=t1w_base, olay=acpc_final, display_mode=orient, save_png=save_png)
        t1wScout_list.append('../anat/{}'.format(save_png.split('/anat/')[-1]))


        # T1wMulEPI to T1w
        save_png = os.path.join(func_pngdir, '{}_T1wMulEPI_{}.png'.format(run_num, orient))        
        plot_anat_w_olay(anat=t1w_base, olay=t1w_mepi, display_mode=orient, save_png=save_png)
        t1mulEpi_list.append('../anat/{}'.format(save_png.split('/anat/')[-1]))

    html_list.append(('Check alignment of Scout2T1w.nii.gz to T1w_acpc_dc_restore.nii.gz', t1wScout_list))
    html_list.append(('Check alignment of T1wMulEPI.nii.gz to T1w_acpc_dc_restore.nii.gz', t1mulEpi_list))



    ### -----------
    ### Check EPI non-linear alignment to group space
    ### -----------
    epi_nonlinmask  = os.path.join(qunex_run.dir_hcp, qunex_run.session_info['id'], str(run_num), '1_nonlin_finalmask.nii.gz')
    t1w_restore     = os.path.join(qunex_run.dir_hcp, qunex_run.session_info['id'], str(run_num), 'OneStepResampling/T1w_restore.2.nii.gz')

    # visualize in all three orientations
    epi_nonlin_list  = []
    for orient in ['x','y','z']:
        # noninear epi alignment
        save_png = os.path.join(func_pngdir, '{}_1_nonlin_finalmask_{}.png'.format(run_num, orient))        
        plot_anat_w_olay(anat=t1w_restore, olay=epi_nonlinmask, display_mode=orient, save_png=save_png)
        epi_nonlin_list.append('../func/{}'.format(save_png.split('/anat/')[-1]))

    html_list.append(('Check alignment of EPI to nonlinear anatomical space', epi_nonlin_list))







def viz_brains(qunex_dirs, out_dir):
    '''
    Produce nibabel visualizations to assess quality of QUNEX processing outputs
    '''

    out_dir   = '/home/ubuntu/embarc_qunex'
    qunex_dir = '/fmri-qunex/research/imaging/datasets/embarc/processed_data/pf-pipelines/qunex-nbridge/studies/embarc-20201122-LHzJPHi4/sessions/MG0066_wk1'
    qunex_run = qunex(qunex_dir)

    # create output directories
    create_odir(out_dir=out_dir, id=qunex_run.session_info['id'])


    anat_qc_images(qunex_run, out_dir)

    make_func_qc_images(qunex_run, out_dir)
