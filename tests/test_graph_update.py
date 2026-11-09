from builderguild.graph import FactGraph


def make_graph(tmp_path):
    return FactGraph(str(tmp_path / "graph.db"))


def test_update_status_changes_status(tmp_path):
    fg = make_graph(tmp_path)
    fact_id = fg.add("Tugas", "ringkasan", {})
    fg.update_status(fact_id, "in_progress")
    rows = fg.list_titles(status="in_progress")
    assert [r["id"] for r in rows] == [fact_id]
    assert fg.list_titles(status="open") == []
    fg.close()


def test_update_status_only_affects_target(tmp_path):
    fg = make_graph(tmp_path)
    first = fg.add("Satu", "s", {})
    second = fg.add("Dua", "s", {})
    fg.update_status(first, "done")
    statuses = {r["id"]: r["status"] for r in fg.list_titles()}
    assert statuses == {first: "done", second: "open"}
    fg.close()


def test_update_status_unknown_id_is_noop(tmp_path):
    fg = make_graph(tmp_path)
    fg.add("Satu", "s", {})
    fg.update_status(999, "done")
    assert [r["status"] for r in fg.list_titles()] == ["open"]
    fg.close()