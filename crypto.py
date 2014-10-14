import hashlib
import hmac
import gnupg
import subprocess

class Cipher(object):
    def __init__(self, key):
        self.key = key

    def encrypt(self, infile, outfile):
        raise Exception("No encryption implemented!")

    def decrypt(self, infile, outfile):
        raise Exception("No decryption implemented!")


class GPGCipher(Cipher):
    def __init__(self, key):
        super(GPGCipher, self).__init__(key)
        self.gpg = gnupg.GPG()

    def encrypt(self, infile, outfile):
        with infile.open(mode="rb") as f:
            self.gpg.encrypt_file(f, recipients=None, symmetric=True, passphrase=self.key, output=str(outfile), armor=False)

    def decrypt(self, infile, outfile):
        with infile.open(mode="rb") as f:
            self.gpg.decrypt_file(f, passphrase=self.key, output=str(outfile))

def gen_filename(hashstr):
    return hmac.new("temp", hashstr, hashlib.sha1).hexdigest()[:20]

if __name__ == "__main__":
    c = GPGCipher("abc")
    c.encrypt("local.json", "out.gpg")
    c.decrypt("out.gpg", "out")

    print gen_filename("a")

def calc_auth(key, ctr):
    h = hmac.new(key, 'sha1')
    h.update(str(ctr))

    return unicode(h.hexdigest())

def secure_compare(x, y):
    if len(x) != len(y):
        return False
    diffs = sum(a != b for a, b in zip(x, y))
    return diffs == 0
