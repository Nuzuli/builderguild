import sqlite3

from builderguild.graph import FactGraph


def test_fact_graph_creates_facts_table(tmp_path):
    db = tmp_path / "graph.db"
    FactGraph(str(db))

    conn = sqlite3.connect(db)
    columns = {row[1] for row in conn.execute("PRAGMA table_info(facts)")}
    conn.close()

    expected = {"id", "title", "summary", "evidence", "kind", "status", "owner", "created", "updated"}
    assert expected <= columns