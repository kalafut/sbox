from collections import namedtuple
import crypto
import hashlib
import os
import py
import json
import uuid
import requests
import cPickle as pickle

from util import read_file
from py.path import local as l


OBJ_ID_LEN = 20

EncryptedFile = namedtuple('EncryptedFile', ['id','filename', 'sha1', 'deleted'])
EncryptedFile.__eq__ = lambda a,b : ((a.id == None or b.id == None) or (a.id == b.id)) and a.filename == b.filename and a.sha1 == b.sha1 and a.deleted == b.deleted

class Catalog:
    def __init__(self, filename=None):
        self.catalog_id = crypto.random_hex(OBJ_ID_LEN)
        self.seq_id = 0

        if not filename:
            self.objects = []
        else:
            with open(filename,"rb") as f:
                self.objects = pickle.load(f)

    def inflate(self, json_str):
        obj = json.loads(json_str)
        self.catalog_id = obj['catalog_id']
        self.seq_id = obj['seq_id']
        self.objects = obj['objects']

    def save(self, filename):
        with open(filename,"wb") as f:
            pickle.dump(self.objects, f)



    def to_json(self):
        obj = {
            'catalog_id': self.catalog_id,
            'seq_id': self.seq_id,
            'objects': self.objects
        }
        return json.dumps(obj)

    def add_file(self, path):
        self.objects.append(
            EncryptedFile(id=crypto.random_hex(OBJ_ID_LEN), filename=path, sha1=py.path.local(path).computehash(hashtype='sha1'), deleted=False)
        )

    def files(self):
        return self.objects.keys()

    def hashes(self):
        [ o['sha1'] for o in self.objects.itervalues() ]

    def find_file(filename):
        for o in self.objects.itervalues():
            if o.location == filename:
                return o
        return None

    @staticmethod
    def compare(local, current, base=None):
        result = {
            'local_add': [],
            'local_del': [],
            }

        l = set(local.ids())
        c = set(current.ids())

        print local.files()

        diffs = l ^ c
        print diffs
        result['local_add'] = list(c - l)
        result['local_del'] = list(l - c)

        return result


    def write(self, filename):
        with open(filename, "wb") as f:
            f.write(self.to_json())


    def add_path(self, path):
        for p in path.visit():
            if p.check(file=1):
                self.add_file(path.bestrelpath(p))


class ClientSet:
    def __init__(self, root):
        self.objects = {}
        self.traverse(root)

    def traverse(self, root):
        for root, dirs, files in os.walk(root):
            for name in files:
                o = PryObject(os.path.join(root, name))
                self.objects[o.id.hexdigest()] = o

class Blob:
    def __init__(self, key, data=None, blob=None):
        if data and blob:
            raise Exception

        self.hmac = HMAC.new(key)
        if data:
            self.data = data
            self.hmac.update(data)
            self.hash = self.hmac
        elif blob:
            self.data = blob[self.hmac.digest_size:]
            self.hash = blob[:self.hmac.digest_size]


    def get_wrapped(self):
        return self.hmac.digest() + self.data


def scan(r):
    fs = []
    for root, dirs, files in os.walk(r):
        for name in files:
            o = PryObject(os.path.join(root, name))
            self.objects[o.id.hexdigest()] = o


def encrypt_folder(source, dest):
    cipher = crypto.GPGCipher("test")
    for p in source.visit():
        if p.check(file=1):
            cipher.encrypt(p, dest / p.basename)

"""
root = "./tmp"

a = PryObject('prybox.py')
c =  ClientSet(root)

for k,v in c.objects.items():
    print v.path
    print k
    print v.hash.hexdigest()
    print

b = Blob("test")
b.add_data("asdfsafa")
print b.get_wrapped()

local = Catalog(json_str=read_file("local.json"))
current = Catalog(json_str=read_file("current.json"))

print Catalog.compare(local, current)

#c = Catalog()
#c.add_path("testbed")
#c.write("test.json")

files = {'local': open('local.json', 'rb')}
r = requests.post("http://127.0.0.1:5000/object", files=files)
r = requests.get("http://127.0.0.1:5000/object/local")
print r.text

"""

#encrypt_folder(l("/tmp/in/"), l("/tmp/out/"))
