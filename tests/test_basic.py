import os
import prybox.prybox
from prybox.prybox import EncryptedFile
from prybox.crypto import GPGCipher
from py.path import local as l

import py

# content of test_sample.py
def func(x):
    return x + 1

def test_answer(tmpdir):
    assert func(3) == 4

def test_add_file(tmpdir):
    p = tmpdir.join("t1")
    p.write("Sample text")
    p = tmpdir.join("t2")
    p.write("Sample text 2")

    c = prybox.prybox.Catalog()

    tmpdir.chdir()
    c.add_file("t1")
    assert len(c.objects)==1
    assert c.objects[0].sha1 == "45aa94d570fb86da79b38a3b7f84f7230c84c01f"


def test_add_path(tmpdir):
    tmpdir.join("t1").write("Sample text")
    tmpdir.join("t2").write("Sample text 2")
    tmpdir.join("subdir", "t3").write("Sample text 3", ensure=True)

    c = prybox.prybox.Catalog()

    tmpdir.chdir()
    c.add_path(py.path.local("."))
    assert len(c.objects)==3

    ef1 = EncryptedFile(id=None, filename="t1", sha1="45aa94d570fb86da79b38a3b7f84f7230c84c01f", deleted=False)
    ef2 = EncryptedFile(id=None, filename="t2", sha1="53a569e56e43968cb548afb376a5a8f8761e09fe", deleted=False)
    ef3 = EncryptedFile(id=None, filename=os.path.normcase("subdir/t3"), sha1="89650e1d956fe16a01cd4de542aadf6cfa563db4", deleted=False)
    assert ef1 in c.objects
    assert ef2 in c.objects
    assert ef3 in c.objects

def test_catalog_save_and_restore(tmpdir):
    tmpdir.join("t1").write("Sample text")
    tmpdir.join("t2").write("Sample text 2")
    tmpdir.join("subdir", "t3").write("Sample text 3", ensure=True)

    c = prybox.prybox.Catalog()

    tmpdir.chdir()
    c.add_path(py.path.local("."))

    c.save("catalog")

    c = prybox.prybox.Catalog("catalog")

    ef1 = EncryptedFile(id=None, filename="t1", sha1="45aa94d570fb86da79b38a3b7f84f7230c84c01f", deleted=False)
    ef2 = EncryptedFile(id=None, filename="t2", sha1="53a569e56e43968cb548afb376a5a8f8761e09fe", deleted=False)
    ef3 = EncryptedFile(id=None, filename=os.path.normcase("subdir/t3"), sha1="89650e1d956fe16a01cd4de542aadf6cfa563db4", deleted=False)
    assert len(c.objects) == 3
    assert ef1 in c.objects
    assert ef2 in c.objects
    assert ef3 in c.objects


def test_encrypt_decrypt(tmpdir):
    tmpdir.join("t1").write("Sample text")

    c1 = GPGCipher("test key")
    c2 = GPGCipher("test key")
    c3 = GPGCipher("test key bad")

    old = tmpdir.chdir()

    c1.encrypt(l("t1"), l("t1.gpg"))
    c2.decrypt(l("t1.gpg"), l("t2"))
    assert tmpdir.join("t1").computehash() != tmpdir.join("t1.gpg").computehash()
    assert tmpdir.join("t1").computehash() == tmpdir.join("t2").computehash()

    # TODO how do we get a return status??
    #c3.decrypt("t1.gpg", "t3")


    old.chdir()


def test_random_id():
    assert len(prybox.prybox.random_id()) == prybox.prybox.OBJ_ID_LEN
