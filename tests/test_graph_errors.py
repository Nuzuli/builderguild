import pytest

from builderguild.errors import GraphError
from builderguild.graph import FactGraph


class _FakeCursor:
    lastrowid = None


class _FakeConn:
    def execute(self, *args, **kwargs):
        return _FakeCursor()

    def commit(self):
        pass

    def close(self):
        pass


def test_add_raises_graph_error_when_no_row_id(tmp_path):
    fg = FactGraph(str(tmp_path / "bg.db"))
    fg.conn.close()
    fg.conn = _FakeConn()
    with pytest.raises(GraphError, match="INSERT gagal"):
        fg.add("judul", "ringkasan", {})