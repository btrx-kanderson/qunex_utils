import os


class qunex(object):
    '''
    Class with functions for wrapping around an individual QUNEX subject directory

    Attributes
    ----------- 
        dir:        Full path to the QUNEX subject directory
        dir_hcp:    Full path to the HCP/QUNEX subject directory
        dir_bids:   Full path to the BIDS/QUNEX subject directory
        dir_nii:    Full path to the NII/QUNEX subject directory

        session_info: Dictionary with metadata about the QUNEX run
        session_txt:  Full path to the QUNEX produced txt file run metadata

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
        folders = ['hcp', 'images', 'bids', 'nii']
        for folder in folders:
            if os.path.exists(os.path.join(self.dir, folder)):
                setattr(self, 'dir_{}'.format(folder), os.path.join(self.dir, folder))

        # there should be a log/txt file with session information
        if os.path.exists(os.path.join(self.dir, 'session.txt')):
            setattr(self, 'session_txt', os.path.join(self.dir, 'session.txt'))
            self._read_session()
            

    def _print(self):
        print(self.dir)