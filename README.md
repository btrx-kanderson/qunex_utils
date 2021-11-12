# qunex-utils

Data mungeing, QC, and visualization wrapper for QUNEX

(1) Compile BOLD head motion estimates
(2) Compile Freesurfer anatomical features
(3) Compile BOLD mask brain coverage


## Installation

Install the package straight from github. 

    sudo pip3 install git+https://github.com/btrx-kanderson/qunex_utils.git


## Running qunex_utils
    
(1) Compile BOLD head motion estimates
(2) Compile Freesurfer anatomical features
(3) Compile BOLD mask brain coverage


## Output

The output directory structure will contain the following: 

    ${out_dir}
        |-- data
            |-- bold_mask_estimates.csv
            |-- bold_motion_estimates.csv
            |-- freesurfer_estimates.csv
        |-- qc
        |-- viz
            |-- pheno_histograms




