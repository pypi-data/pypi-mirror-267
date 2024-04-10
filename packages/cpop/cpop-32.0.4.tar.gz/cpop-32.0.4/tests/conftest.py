import pathlib
import sys
import unittest.mock as mock

import pop.hub
import pytest


@pytest.fixture()
async def hub():
    yield await pop.hub.AsyncHub(
        # Let each test manually add their structure
        load_all_dynes=False,
        load_all_subdirs=False,
        recurse_subdirs=False,
        logs=False,
        load_config=False,
    )


@pytest.fixture(autouse=True, scope="session")
def tpath():
    code_dir = pathlib.Path(__file__).parent.parent.absolute()
    assert code_dir.exists()

    tpath_dir = code_dir / "tests" / "tpath"
    assert tpath_dir.exists()

    NEW_PATH = [str(code_dir), str(tpath_dir)]

    for p in sys.path:
        if p not in NEW_PATH:
            NEW_PATH.append(p)

    with mock.patch("sys.path", NEW_PATH):
        yield
