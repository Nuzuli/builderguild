from builderguild import cli


def test_add_creates_task(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("BG_DB_PATH", str(tmp_path / "bg.db"))
    assert cli.main(["add", "Perbaiki bug", "--detail", "login gagal"]) == 0
    cli.main(["status"])
    assert "Perbaiki bug" in capsys.readouterr().out