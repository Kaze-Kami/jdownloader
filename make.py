import os
import shutil
from pathlib import Path

import sys

if __name__ == '__main__':
    from_dir = Path(os.path.dirname(__file__))
    root_dir = Path(sys.argv[1]) if 1 < len(sys.argv) else from_dir
    root_dir = root_dir.joinpath('make/jdownloader/')
    bin_dir = root_dir.joinpath('bin/')
    if root_dir.exists():
        shutil.rmtree(root_dir)
    else:
        root_dir.mkdir()

    shutil.copytree(from_dir.joinpath('src'), bin_dir.joinpath('src'))
    shutil.copy(from_dir.joinpath('main.py'), bin_dir.joinpath('main.py'))
    shutil.copy(from_dir.joinpath('setup.py'), root_dir.joinpath('setup.py'))
    shutil.copy(from_dir.joinpath('remove_jacked_files.py'), root_dir.joinpath('remove_jacked_files.py'))
    shutil.copy(from_dir.joinpath('README.txt'), root_dir.joinpath('README.txt'))
