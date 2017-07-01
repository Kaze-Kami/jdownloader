# resources
from os.path import dirname
from pathlib import Path

my_path = Path(dirname(__file__))
root = my_path.parent
resources_path = root.joinpath('resources/')
log_path = resources_path.joinpath('logs/')

# tor
tor_path = root.joinpath('src/tor_bundle/Tor/tor.exe')
tor_data_dir = resources_path.joinpath('tor_data/')

tor_password_hashed = '16:D93AEAD2300D037460B041C34A335BF8A5ECE6C142862F06344C3F8D8C'
tor_password = 'I want control!'


# ensure resources path
if not resources_path.exists():
    resources_path.mkdir()
if not log_path.exists():
    log_path.mkdir()
if not tor_data_dir.exists():
    tor_data_dir.mkdir()
