from pathlib import Path

from os import path, remove


def create_bat(path, main_path, output_path, get_path, l1, l2, debug_level):
    with open(path, 'w') as f:
        f.write('python "%s" "%s" "%s" "%d" "%d" "%s"\nPAUSE' % (main_path, get_path, output_path, l1, l2, debug_level))


if __name__ == '__main__':
    # start bat with high and low load aswell as one with debug level
    # folder structure as some_dir/root_dir
    # with bin/(already here), downloads, start_bat_...,
    root_dir = Path(path.dirname(__file__))
    # target path = m_dir/..
    # as structure should be some_dir/root/setup.py
    dl_dir = root_dir.joinpath('downloads/')
    main_path = root_dir.joinpath('bin/main.py')
    get_path = root_dir.joinpath('to_get.txt')

    if not dl_dir.exists():
        dl_dir.mkdir()

    if not get_path.exists():
        open(get_path, 'w')

    create_bat(root_dir.joinpath('run_high.bat'), main_path, dl_dir, get_path, 5, 20, 'MINIMAL')
    # create_bat(root_dir.joinpath('run_high_debug.bat'), main_path, dl_dir, get_path, 5, 20, 'DEBUG')
    # create_bat(root_dir.joinpath('run_high_quiet.bat'), main_path, dl_dir, get_path, 5, 20, 'QUIET')
    create_bat(root_dir.joinpath('run_low.bat'), main_path, dl_dir, get_path, 1, 5, 'MINIMAL')
    # create_bat(root_dir.joinpath('run_low_debug.bat'), main_path, dl_dir, get_path, 1, 5, 'DEBUG')
    # create_bat(root_dir.joinpath('run_low_quiet.bat'), main_path, dl_dir, get_path, 1, 5, 'QUIET')

    remove(root_dir.joinpath('setup.py'))
