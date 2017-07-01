import sys
from pathlib import Path

from src.AnimeDownloader import AnimeDownloader
from src.downloading.anime_downloader import anime_download_manager
from src.downloading.file_downloader import download_manager
from src.util.logging.logger import set_global_log_level, LogLevel, log, MessageType, MessageLevel


def run(parse_limit, download_limit, get_file_path, base_save_path, log_level):
    log('Starting downloader. Config:', MessageType.SYSTEM, MessageLevel.SYSTEM)
    log('Log level: %s' % log_level.name, MessageType.SYSTEM, MessageLevel.SYSTEM)
    log('Get file: %s' % get_file_path, MessageType.SYSTEM, MessageLevel.SYSTEM)
    log("Save path: %s" % base_save_path, MessageType.SYSTEM, MessageLevel.SYSTEM)
    log("parse limit: %d" % parse_limit, MessageType.SYSTEM, MessageLevel.SYSTEM)
    log("download limit: %d" % download_limit, MessageType.SYSTEM, MessageLevel.SYSTEM)
    set_global_log_level(log_level)
    download_manager.set_download_limit(download_limit)
    anime_download_manager.set_download_limit(parse_limit)
    anime_downloader = AnimeDownloader(get_file_path, base_save_path)
    anime_downloader.start()


def run_from_console():
    args = sys.argv
    get_path = Path(args[1])
    save_path = Path(args[2])
    parser_limit = int(args[3]) if 3 < len(args) else -1
    downloader_limit = int(args[4]) if 4 < len(args) else -1
    log_level = LogLevel[args[5]] if 5 < len(args) else LogLevel.NORMAL
    run(parser_limit, downloader_limit, get_path, save_path, log_level)


if __name__ == '__main__':
    run_from_console()
