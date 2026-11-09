from builderguild import cli


def test_status_filter_only_done(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("BG_DB_PATH", str(tmp_path / "bg.db"))
    cli.main(["add", "Tugas Alpha"])
    cli.main(["add", "Tugas Beta"])
    cli.main(["done", "1"])
    capsys.readouterr()

    cli.main(["status", "--filter", "done"])
    out = capsys.readouterr().out
    assert "Tugas Alpha" in out
    assert "Tugas Beta" not in out


def test_status_without_filter_shows_all(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("BG_DB_PATH", str(tmp_path / "bg.db"))
    cli.main(["add", "Tugas Alpha"])
    cli.main(["add", "Tugas Beta"])
    capsys.readouterr()

    cli.main(["status"])
    out = capsys.readouterr().out
    assert "Tugas Alpha" in out
    assert "Tugas Beta" in out