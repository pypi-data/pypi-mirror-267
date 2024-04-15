import pathlib
import sys
from unittest import mock

import cpop.hub
import pytest


@pytest.fixture(name="hub")
async def testing_hub():
    async with cpop.hub.Hub() as hub:
        yield hub


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
