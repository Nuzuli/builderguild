import pytest

from builderguild.cli import main


def test_setup_creates_graph(tmp_path, monkeypatch, capsys):
    db = tmp_path / "graph.db"
    monkeypatch.setenv("BG_DB_PATH", str(db))
    assert main(["setup"]) == 0
    assert db.exists()
    assert "[setup] graph siap" in capsys.readouterr().out


def test_status_lists_facts_after_setup(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("BG_DB_PATH", str(tmp_path / "graph.db"))
    main(["setup"])
    capsys.readouterr()
    assert main(["status"]) == 0
    out = capsys.readouterr().out
    assert "Setup awal" in out
    assert "[open]" in out


def test_status_on_empty_graph_prints_nothing(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("BG_DB_PATH", str(tmp_path / "graph.db"))
    assert main(["status"]) == 0
    assert capsys.readouterr().out == ""


def test_missing_command_exits_with_code_2():
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 2