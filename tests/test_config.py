import py
import ConfigParser
import sbox.config as config

def test_read_config_trivial(tmpdir):
    sample_cfg = """
[Section 1]
key_1 = value_1
key_2 =    String with spaces

[Section 2]
key_3 : 42
    """

    ini = tmpdir.join('config.ini')
    ini.write(sample_cfg)
    config = ConfigParser.SafeConfigParser()
    config.read(str(ini))

    assert len(config.sections())==2
    for s in ["Section 1", "Section 2"]:
        assert config.has_section(s)

    assert config.get('Section 1', 'key_1')=='value_1'
    assert config.get('Section 1', 'key_2')=='String with spaces'
    assert config.getint('Section 2', 'key_3')==42

    config.set('Section 1', 'key_1', 'Something else')
    config.remove_section('Section 1')
    with open("d:\\test.ini", 'w') as f:
        config.write(f)

def test_generate_config(tmpdir):
    ini = tmpdir.join('config.ini')
    config.generate_config(str(ini))
    print ini.read()
