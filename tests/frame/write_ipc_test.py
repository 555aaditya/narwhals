from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING

import pytest
from packaging.version import Version as PkgVersion

import narwhals as nw
from tests.utils import PANDAS_VERSION

if TYPE_CHECKING:
    from pathlib import Path

    from tests.utils import ConstructorEager

pytest.importorskip("pyarrow")
import pyarrow as pa

data = {"a": [1, 2, 3], "b": ["x", "y", None]}


@pytest.mark.skipif(PANDAS_VERSION < PkgVersion("2"), reason="too old for pyarrow")
@pytest.mark.filterwarnings("ignore:.*is_sparse is deprecated:DeprecationWarning")
def test_write_ipc(constructor_eager: ConstructorEager, tmp_path: Path) -> None:
    df = nw.from_native(constructor_eager(data), eager_only=True)
    path = tmp_path / "foo.arrow"
    df.write_ipc(path)
    assert pa.ipc.open_file(str(path)).read_all().to_pydict() == data

    buffer = BytesIO()
    df.write_ipc(buffer)
    assert pa.ipc.open_file(buffer).read_all().to_pydict() == data
