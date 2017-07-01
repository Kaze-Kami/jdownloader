def remove_line(file, line_text):
    # get line number
    with open(file, 'r') as rf:
        lines = rf.readlines()
    with open(file, 'w') as wf:
        for l in lines:
            if l != line_text + '\n':
                wf.write(l)
