from pathlib import Path

from os import path, remove


def create_bat(path, rel_main_path, rel_output_path, rel_get_path, l1, l2, log_level):
    with open(path, 'w') as f:
        f.write('set cur_dir=%~dp0')
        f.write('\nset main_path=%cur_dir%' + str(rel_main_path))
        f.write('\nset get_path=%cur_dir%' + str(rel_get_path))
        f.write('\nset output_path=%cur_dir%' + str(rel_output_path))
        f.write('\npython "%s" "%s" "%s" "%s" "%s" "%s"\nPAUSE' % ('%main_path%', '%get_path%', '%output_path%', str(l1), str(l2), log_level))


if __name__ == '__main__':
    # start bat with high and low load aswell as one with debug level
    # folder structure as some_dir/root_dir
    # with bin/(already here), downloads, start_bat_...,
    root_dir = Path(path.dirname(__file__))
    # target path = m_dir/..
    # as structure should be some_dir/root/setup.py
    dl_dir = Path('downloads/')
    main_path = Path('bin/main.py')
    get_path = Path('to_get.txt')

    if not dl_dir.exists():
        dl_dir.mkdir()

    if not get_path.exists():
        open(get_path, 'w')

    create_bat(root_dir.joinpath('run_high.bat'), main_path, dl_dir, get_path, 5, 20, 'MINIMAL')
    create_bat(root_dir.joinpath('run_low.bat'), main_path, dl_dir, get_path, 1, 5, 'MINIMAL')
    create_bat(root_dir.joinpath('run_custom.bat'), main_path, 'output_directory', 'get_file_path', 'ACTIVE_PARSES', 'ACTIVE_DOWNLOAD', 'LOG_LEVEL')

    remove(root_dir.joinpath('setup.py'))