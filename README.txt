JDownloader by KanjiuAkuma

Setup:
    install python3 if not present
        -> https://www.python.org/ftp/python/3.6.1/python-3.6.1.exe
    run the setup.py file

Usage:
    paste index urls of the animes you want into the to_get.txt
        eg (http://animeheaven.eu/i.php?a=Clockwork%20Planet%20Dubbed)
    if you want do download an ongoing anime use the '-o' parameter so the downloader keeps checking even if the anime was completely downloaded once
        eg (-o http://animeheaven.eu/i.php?a=Clockwork%20Planet%20Dubbed)
    your downloads will be located in the downloads directory

    use either use run_high.bat or run_low.bat or setup the run_custom.bat to start (low for less network usage, high for more)

    run_custom:
        1. parameter should be left unchanged.
        2. parameter is the get_file you want to use, i suggest using the one automatically created by the setup.py
        3. parameter is the output directory
        4. parameter is how many animes are parsed and initiated at a time (not that important in terms of network usage but keep it between 2 and 15 for a smooth download process)
        5. parameter is how many downloads may be active at a time
        6. parameter is the log level
            available options:
                QUIET (Errors, warnings)
                HUSH (Errors, warnings, system messages)
                MINIMAL (Errors, warnings, system messages, minimal progress info)
                NORMAL (Errors, warnings, system messages, progress info)
                FULL (Errors, warnings, system messages, full progress info)
                DEBUG (Errors, warnings, system messages, full progress info, debug info)
                ALL (...)
