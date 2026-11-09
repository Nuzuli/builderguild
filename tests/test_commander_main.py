import commander
from builderguild.errors import TmuxNotAvailableError


def test_main_dispatches_tasks(monkeypatch, tmp_path):
    monkeypatch.setenv("BG_DB_PATH", str(tmp_path / "bg.db"))
    spawned, told = [], []
    monkeypatch.setattr(
        commander, "spawn_tmux", lambda name, cmd="bash": spawned.append(name) or True
    )
    monkeypatch.setattr(
        commander, "tell_tmux", lambda name, text: told.append((name, text))
    )
    commander.main()
    assert spawned == ["bg-soldier"]
    assert len(told) == 2


def test_main_stops_when_tmux_missing(monkeypatch, tmp_path):
    monkeypatch.setenv("BG_DB_PATH", str(tmp_path / "bg.db"))
    told = []

    def fake_spawn(name, cmd="bash"):
        raise TmuxNotAvailableError("tmux belum diinstall!")

    monkeypatch.setattr(commander, "spawn_tmux", fake_spawn)
    monkeypatch.setattr(
        commander, "tell_tmux", lambda name, text: told.append((name, text))
    )
    commander.main()
    assert told == []