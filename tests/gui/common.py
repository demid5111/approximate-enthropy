import os


def check_report(path):
    assert os.path.exists(path)

    with open(path) as f:
        content = f.read()
        assert 'error' not in content
