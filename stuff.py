def truncate_get_file(url, get_file_path):
    with open(get_file_path, 'r') as rf:
        lines = rf.readlines()
    last_comment = 0
    for i, l in enumerate(lines):
        if 'http' in l:
            break
        elif l[0] == '#':
            last_comment = i

    with open(get_file_path, 'w') as wf:
        for l in lines[last_comment:]:
            if l != url + '\n':
                wf.write(l)


if __name__ == '__main__':
    truncate_get_file('http://animeheaven.eu/i.php?a=Code%20Geass%20-%20Lelouch%20of%20the%20Rebellion%20R2',
                      r'D:\Dev\PyCharm Projects\JDownloader_4.0\resources\get_file_high.txt')
