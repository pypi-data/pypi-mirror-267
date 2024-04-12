import sys
import unittest.mock as mock

import aiopath
import cpop.hub
import pytest


@pytest.fixture(name="hub")
async def testing_hub():
    yield await cpop.hub.AsyncHub()


@pytest.fixture(autouse=True, scope="session")
async def tpath():
    code_dir = await aiopath.AsyncPath(__file__).parent.parent.absolute()
    assert await code_dir.exists()

    tpath_dir = code_dir / "tests" / "tpath"
    assert await tpath_dir.exists()

    NEW_PATH = [str(code_dir), str(tpath_dir)]

    for p in sys.path:
        if p not in NEW_PATH:
            NEW_PATH.append(p)

    with mock.patch("sys.path", NEW_PATH):
        yield
