# -*- coding: utf-8 -*-
# 06/20/2023: created, finalized

import sys
import os
cd = os.path.dirname(__file__)
sys.path.append('dap-py')
import warnings
from datetime import datetime
from doe_dap_dl import DAP
warnings.filterwarnings("ignore")

#%% Inputs
username = ''#ask DAP (dapteam@pnnl.gov)
password = ''
channels = {'lidar1': 'raaw/nrel.lidar.z01.b0','lidar2': 'raaw/nrel.lidar.z02.b0',
            'met': 'raaw/ge.met.z01.b0', 'scada': 'raaw/ge.turbine.z01.b0'}
MFA = True #multi factor authenticaiton needed? this is necessary for propietary datasets

#%% Main
t_start=input('Start time (%Y-%m-%d %H:%M):')
t_end=  input('End time (%Y-%m-%d %H:%M):')

time_range_dap = [datetime.strftime(datetime.strptime(t_start, '%Y-%m-%d %H:%M'), '%Y%m%d%H%M%S'),
                  datetime.strftime(datetime.strptime(t_end, '%Y-%m-%d %H:%M'), '%Y%m%d%H%M%S')]

a2e = DAP('a2e.energy.gov',confirm_downloads=False)
if MFA:
    a2e.setup_two_factor_auth(username=username, password=password)
else:
    a2e.setup_cert_auth(username=username, password=password)

for k in channels.keys():
    # download data
    destination = os.path.join('data',channels[k])
    os.makedirs(destination)
    filter = {
        'Dataset': channels[k],
        'date_time': {
            'between': time_range_dap
        },
        'file_type': 'nc'
    }
    a2e.download_with_order(filter, path=destination, replace=False)
input('Press enter...')
