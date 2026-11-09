import commander


class _Result:
    def __init__(self, returncode):
        self.returncode = returncode


def test_session_exists_true(monkeypatch):
    monkeypatch.setattr(commander.subprocess, "run", lambda *a, **k: _Result(0))
    assert commander.session_exists("bg-test") is True


def test_session_exists_false(monkeypatch):
    monkeypatch.setattr(commander.subprocess, "run", lambda *a, **k: _Result(1))
    assert commander.session_exists("bg-test") is False


def test_spawn_tmux_without_tmux(monkeypatch, capsys, caplog):
    monkeypatch.setattr(commander.shutil, "which", lambda name: None)
    assert commander.spawn_tmux("bg-test") is False
    output = capsys.readouterr().out + caplog.text
    assert "tmux belum diinstall" in output


def test_spawn_tmux_creates_session(monkeypatch):
    calls = []
    monkeypatch.setattr(commander.shutil, "which", lambda name: "/usr/bin/tmux")
    monkeypatch.setattr(commander, "session_exists", lambda name: False)
    monkeypatch.setattr(commander.subprocess, "run", lambda cmd, **k: calls.append(cmd))
    assert commander.spawn_tmux("bg-test", "bash") is True
    assert calls == [["tmux", "new-session", "-d", "-s", "bg-test", "bash"]]


def test_tell_tmux_sends_keys(monkeypatch):
    calls = []
    monkeypatch.setattr(commander, "session_exists", lambda name: True)
    monkeypatch.setattr(commander.subprocess, "run", lambda cmd, **k: calls.append(cmd))
    commander.tell_tmux("bg-test", "halo")
    assert calls == [["tmux", "send-keys", "-t", "bg-test", "halo", "Enter"]]


def test_tell_tmux_skips_missing_session(monkeypatch):
    calls = []
    monkeypatch.setattr(commander, "session_exists", lambda name: False)
    monkeypatch.setattr(commander.subprocess, "run", lambda cmd, **k: calls.append(cmd))
    commander.tell_tmux("bg-test", "halo")
    assert calls == []