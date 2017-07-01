import os
import shutil
from pathlib import Path

if __name__ == '__main__':
    root = Path(os.path.dirname(__file__))
    target = root.joinpath('bin')
    if target.exists():
        shutil.rmtree(target)
    else:
        target.mkdir()

    shutil.copytree(root.joinpath('src'), target.joinpath('src'))
    shutil.copytree(root.joinpath('tor_bundle'), target.joinpath('tor_bundle'))
    shutil.copy(root.joinpath('main.py'), target.joinpath('main.py'))
    shutil.copy(root.joinpath('AnimeDownloader.py'), target.joinpath('AnimeDownloader.py'))
