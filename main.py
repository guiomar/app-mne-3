# Copyright (c) 2020 brainlife.io
#
# This file is a MNE python-based brainlife.io App
#
# Author: Guiomar Niso
# Indiana University

# Required libraries
# pip install mne-bids coloredlogs tqdm pandas scikit-learn json_tricks fire

# set up environment
#import mne-study-template
import os
import json
from shutil import copyfile
from distutils.dir_util import copy_tree

# Current path
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Path to mne-study-template 
#mnest_path = '/Users/guiomar/Documents/GitHub/mne-bids-pipeline'
mnest_path = '/mne-bids-pipeline'

# Populate mne_config.py file with brainlife config.json
with open(__location__+'/config.json') as config_json:
    config = json.load(config_json)


bids_root = str(config['output']) 
deriv_root = 'out_dir'

# Copy the input folder ('output') in the output folder ('out_dir') to have all the data there
copy_tree(bids_root, os.path.join(__location__,"out_dir"))


'''
#study_name = 'ds000246'
bids_root = str(config['output']) # '/Users/guiomar/Projects/ds000246'
deriv_root = 'out_dir'
subjects = ['0001']

l_freq = .3
h_freq = 100.
decim = 10 #4
reject = dict(mag=4e-12, eog=250e-6)
conditions = ['standard', 'deviant', 'button']


contrasts = [('deviant', 'standard')]
decode = True
daysback = -365 * 110
on_error = 'debug'

'''


'''
#study_name = 'ds000248'
subjects = ['01']
rename_events = {'Smiley': 'Emoji','Button': 'Switch'}
conditions = ['Auditory', 'Visual', 'Auditory/Left', 'Auditory/Right']
ch_types = ['meg']
#mf_reference_run = '1' ##bl2bids just 1 not 01
find_flat_channels_meg = True
find_noisy_channels_meg = True
use_maxwell_filter = True
process_er = True
reject = dict(mag=4e-12, eog=250e-6)

contrasts = [('Visual', 'Auditory'),('Auditory/Right', 'Auditory/Left')]
bem_mri_images = 'FLASH'
recreate_bem = True
noise_cov = 'emptyroom'


'''

# Create new MNE config .py file

fname = 'mne_config.py'

with open(fname, 'w') as f: 

    # == GENERAL SETTINGS ==

    f.write("bids_root = '{}'".format(bids_root)+'\n')
    f.write("deriv_root = '{}'".format(deriv_root)+'\n')
    #For freesurfer
    '''
    if config['subjects_dir']:      f.write('subjects_dir = {}'.format(config['subjects_dir'])+'\n')

    if config['study_name']:        f.write('study_name = {}'.format(config['study_name'])+'\n')
    if config['interactive']:       f.write('interactive = {}'.format(config['interactive'])+'\n')
    if config['crop']:              f.write('crop = {}'.format(config['crop'])+'\n')
 
    if config['sessions']:          f.write('sessions = {}'.format(config['sessions'])+'\n')
    if config['task']:              f.write('task = {}'.format(config['task'])+'\n')
    if config['runs']:              f.write('runs = {}'.format(config['runs'])+'\n')
    if config['acq']:               f.write('acq = {}'.format(config['acq'])+'\n')
    if config['proc']:              f.write('proc = {}'.format(config['proc'])+'\n')
    if config['rec']:               f.write('rec = {}'.format(config['rec'])+'\n')
    if config['space']:             f.write('space = {}'.format(config['space'])+'\n')
    if config['subjects']:          f.write('subjects = {}'.format(config['subjects'])+'\n')
    if config['exclude_subjects']:  f.write('exclude_subjects = {}'.format(config['exclude_subjects'])+'\n')
    '''
    #if config['process_er']:        f.write('process_er = {}'.format(config['process_er'])+'\n')
    if config['ch_types']:          f.write("ch_types = {}".format(config['ch_types'])+'\n')
    if config['data_type']:         f.write("data_type = {}".format(config['data_type'])+'\n')
    if config['eog_channels']:      f.write('eog_channels = {}'.format(config['eog_channels'])+'\n')
    if config['eeg_bipolar_channels']:  f.write('eeg_bipolar_channels = {}'.format(config['eeg_bipolar_channels'])+'\n')
    if config['eeg_reference']:     f.write("eeg_reference = '{}'".format(config['eeg_reference'])+'\n')
    if config['eeg_template_montage']:  f.write('eeg_template_montage = {}'.format(config['eeg_template_montage'])+'\n')
    if config['drop_channels']:     f.write('drop_channels = {}'.format(config['drop_channels'])+'\n')
    if config['analyze_channels']:  f.write('analyze_channels = {}'.format(config['analyze_channels'])+'\n')
 

    # SOURCES

    # General Settings
    if config['run_source_estimation']: f.write("run_source_estimation = {}".format(config['run_source_estimation'])+'\n')

    # BEM surface
    if config['bem_mri_images']:        f.write("bem_mri_images = {}".format(config['bem_mri_images'])+'\n')
    if config['recreate_bem']:          f.write("recreate_bem = {}".format(config['recreate_bem'])+'\n')

    # Source space & forward solution
    if config['mri_t1_path_generator']: f.write("mri_t1_path_generator = {}".format(config['mri_t1_path_generator'])+'\n')
    if config['spacing']:               f.write("spacing = {}".format(config['spacing'])+'\n')
    if config['mindist']:               f.write("mindist = {}".format(config['mindist'])+'\n')

    # Inverse solution
    if config['inverse_method']:    f.write("inverse_method = {}".format(config['inverse_method'])+'\n')
    if config['noise_cov']:         f.write("noise_cov = {}".format(config['noise_cov'])+'\n')

    f.close() 


# Run mne-study-template python script
os.system( mnest_path + '/run.py --config=' + __location__+'/mne_config.py \
    --steps=sensor,report/make_reports.py')


# Find the reports and make a copy in out_html folder
for dirpath, dirnames, filenames in os.walk(__location__+"/out_dir"):
    for filename in [f for f in filenames if f.endswith(".html")]:
        if not "sub-average" in filename:
            print(filename)
            copyfile(os.path.join(__location__,"out_dir", dirpath,filename), os.path.join(__location__,"html_report",filename))