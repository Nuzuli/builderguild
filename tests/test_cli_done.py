from builderguild import cli


def test_done_marks_task(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("BG_DB_PATH", str(tmp_path / "bg.db"))
    cli.main(["add", "Perbaiki bug"])
    assert cli.main(["done", "1"]) == 0
    cli.main(["status"])
    assert "[done]" in capsys.readouterr().out


def test_done_unknown_id(monkeypatch, tmp_path):
    monkeypatch.setenv("BG_DB_PATH", str(tmp_path / "bg.db"))
    assert cli.main(["done", "999"]) == 1