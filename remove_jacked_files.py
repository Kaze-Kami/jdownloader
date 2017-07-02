import os
from pathlib import Path

if __name__ == '__main__':
    path = Path(os.path.dirname(__file__)).joinpath('downloads/')
    for d in path.iterdir():
        for f in d.iterdir():
            if f.name == 'jacked':
                os.remove(f)
