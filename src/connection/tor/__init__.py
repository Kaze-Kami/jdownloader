import os
import shutil

import psutil

from src.etc import tor_data_dir

pre_clean_up = True
assure_no_tor = True

# clean up running tor processes
if assure_no_tor:
    for p in psutil.process_iter():
        if p.name() == 'tor.exe':
            p.kill()

# clean up tor data
if not os.path.exists(tor_data_dir):
    os.mkdir(tor_data_dir)
elif pre_clean_up:
    shutil.rmtree(tor_data_dir)
    os.mkdir(tor_data_dir)
