from builderguild.graph import FactGraph


def make_graph(tmp_path):
    return FactGraph(str(tmp_path / "graph.db"))


def test_add_returns_incrementing_ids(tmp_path):
    fg = make_graph(tmp_path)
    first = fg.add("Judul 1", "Ringkasan", {"a": 1})
    second = fg.add("Judul 2", "Ringkasan", {"b": 2})
    assert second == first + 1
    fg.close()


def test_list_titles_returns_all(tmp_path):
    fg = make_graph(tmp_path)
    fg.add("Satu", "s", {}, owner="scout")
    fg.add("Dua", "s", {})
    rows = fg.list_titles()
    assert [r["title"] for r in rows] == ["Satu", "Dua"]
    assert rows[0]["owner"] == "scout"
    assert rows[0]["status"] == "open"
    fg.close()


def test_list_titles_filters_by_status(tmp_path):
    fg = make_graph(tmp_path)
    fg.add("Satu", "s", {})
    assert len(fg.list_titles(status="open")) == 1
    assert fg.list_titles(status="done") == []
    fg.close()


def test_list_titles_empty(tmp_path):
    fg = make_graph(tmp_path)
    assert fg.list_titles() == []
    fg.close()