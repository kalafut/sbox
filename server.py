import argparse
import hmac
import os
import py

import flask
import crypto
from flask import Flask, request, g
from util import read_file

app = Flask(__name__)

@app.route("/")
def hello():
    print app.config["obj_dir"]
    return "Hello World!"


@app.route('/object/<refname>', methods=['get'])
def object_get(refname):
    ctr = int(request.args.get('ctr','0'))
    auth = request.args.get('auth','')
    srv_auth = crypto.calc_auth("key", ctr)

    if crypto.secure_compare(auth, srv_auth):
        return root().join(refname).read()
    else:
        return "", 401


@app.route('/object', methods=['POST'])
def object_post():
    if request.method == 'POST':
        name = request.files.keys()[0]
        f = request.files[name]
        f.save(os.path.join(OBJ_DIR, name))

    return ""

def root():
    return app.config["obj_dir"]

def prepare_test():
    tmp_root = py.path.local.mkdtemp()
    py.path.local("tests/server_data").copy(tmp_root)
    return tmp_root

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action="store_true", help="Start server in test mode")

    args = parser.parse_args()

    if args.t:
        app.config["obj_dir"] = prepare_test()
    else:
        app.config["obj_dir"] = py.path.local(".")

    app.debug = True
    app.run()
