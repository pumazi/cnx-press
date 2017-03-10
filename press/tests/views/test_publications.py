# -*- coding: utf-8 -*-
import pathlib
import tempfile
import zipfile

import pytest
from webtest import TestApp

from litezip.tests.conftest import datadir as actual_litezip_datadir


@pytest.fixture(scope='module')
def litezip_datadir():
    return actual_litezip_datadir()


@pytest.fixture
def webapp():
    """Creates a WebTest application for functional testing."""
    from press.main import make_app
    app = make_app()
    return TestApp(app)


def ls_all(p):
    """List all path children"""
    if not p.is_dir():
        yield p
        raise StopIteration()
    for x in p.iterdir():
        if x.is_dir():
            yield from ls_all(x)
        else:
            yield x
    raise StopIteration()


def zip_it(d, zip_filepath):
    """zip up `d` into `zip_filepath`"""
    with zipfile.ZipFile(zip_filepath, 'w') as zb:
        for p in ls_all(d):
            zb.write(str(p))


@pytest.fixture(scope='module')
def stable_litezip(litezip_datadir):
    data_path = litezip_datadir / 'litezip'
    zip_filepath = pathlib.Path(tempfile.mkstemp('.zip')[1])
    zip_it(data_path, str(zip_filepath))
    yield zip_filepath
    zip_filepath.unlink()


@pytest.fixture(scope='module')
def unstable_litezip(litezip_datadir):
    data_path = litezip_datadir / 'invalid_litezip'
    zip_filepath = pathlib.Path(tempfile.mkstemp('.zip')[1])
    zip_it(data_path, str(zip_filepath))
    yield zip_filepath
    zip_filepath.unlink()


def test_post_stable(webapp, stable_litezip):
    upload_files = [('litezip', 'content.zip',
                     stable_litezip.open('rb').read(),)
                    ]
    resp = webapp.post('/publications', upload_files=upload_files)
    assert resp.status_code == 202


def test_post_unstable(webapp, unstable_litezip):
    upload_files = [('litezip', 'content.zip',
                     unstable_litezip.open('rb').read(),)
                    ]
    resp = webapp.post('/publications', upload_files=upload_files)
    assert resp.status_code == 202
