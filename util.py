def read_file(filename):
    s = ""
    with open(filename) as f:
        s = f.read()

    return s
