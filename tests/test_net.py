from prybox.net import Net
import pytest

@pytest.mark.skipif(True, reason="TBD")
def test_get(tmpdir):
    n = Net("http://127.0.0.1:5000")

    f = tmpdir / 'test_file1'
    n.get(f)
    assert f.check(file=1)
