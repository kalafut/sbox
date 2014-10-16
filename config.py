import crypto
import ConfigParser

KEYLEN = 80

def load_config(filename):
    config = ConfigParser.SafeConfigParser()
    config.read(filename)

    config.add_section('Section1')
    config.set('Section1', 'an_int', '15')
    config.set('Section1', 'a_bool', 'true')
    config.set('Section1', 'a_float', '3.1415')
    config.set('Section1', 'baz', 'fun')
    config.set('Section1', 'bar', 'Python')
    config.set('Section1', 'foo', '%(bar)s is %(baz)s!')

    # Writing our configuration file to 'example.cfg'
    with open('example.cfg', 'wb') as configfile:
        config.write(configfile)


def generate_config(filename):
    config = ConfigParser.SafeConfigParser()


    config.add_section('Crypto')
    config.add_section('Local Folders')
    config.set('Crypto', 'encryption_folder', 'c:\\dropbox')
    config.set('Crypto', 'passphrase', crypto.random_key(KEYLEN))

    with open(filename, 'w') as f:
        config.write(f)
