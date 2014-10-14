def import_remote(local, remote):
    for f in remote.files():
        if not local.has_file(f):
            local.add_object(f, remote.get_object(f))


def update(local, current):
    for f in local.files():
        if not current.has_file(f):
            # TODO get and install object here
            


def install(filename):
    target_dir = tempfile.mkdtemp
    filename = net.request( hash stuff, target_dir)
    decrypt(filename)
    #check hash
    #copy file to correct location
    #delete file
    os.rmdir(target_dir)
