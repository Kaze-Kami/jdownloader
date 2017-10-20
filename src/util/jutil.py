import re


def remove_line(file, line_text):
    # get line number
    with open(file, 'r') as rf:
        lines = rf.readlines()
    with open(file, 'w') as wf:
        for l in lines:
            if l != line_text + '\n':
                wf.write(l)


def to_usable_path(a_name):
    res = re.sub('[<>:"/\\\|?!]', '', a_name)
    while res[-1] == ' ' or res[-1] == '.':
        res = res[:-1]
    return res
