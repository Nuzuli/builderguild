import subprocess

import pytest

import commander
from builderguild.errors import TmuxError, TmuxNotAvailableError


class _Result:
    def __init__(self, returncode):
        self.returncode = returncode


def _raise_called_process_error(cmd, **kwargs):
    raise subprocess.CalledProcessError(1, cmd, stderr=b"boom")


def test_session_exists_true(monkeypatch):
    monkeypatch.setattr(commander.subprocess, "run", lambda *a, **k: _Result(0))
    assert commander.session_exists("bg-test") is True


def test_session_exists_false(monkeypatch):
    monkeypatch.setattr(commander.subprocess, "run", lambda *a, **k: _Result(1))
    assert commander.session_exists("bg-test") is False


def test_spawn_tmux_without_tmux(monkeypatch):
    monkeypatch.setattr(commander.shutil, "which", lambda name: None)
    with pytest.raises(TmuxNotAvailableError, match="tmux belum diinstall"):
        commander.spawn_tmux("bg-test")


def test_spawn_tmux_creates_session(monkeypatch):
    calls = []
    monkeypatch.setattr(commander.shutil, "which", lambda name: "/usr/bin/tmux")
    monkeypatch.setattr(commander, "session_exists", lambda name: False)
    monkeypatch.setattr(commander.subprocess, "run", lambda cmd, **k: calls.append(cmd))
    assert commander.spawn_tmux("bg-test", "bash") is True
    assert calls == [["tmux", "new-session", "-d", "-s", "bg-test", "bash"]]


def test_spawn_tmux_skips_existing_session(monkeypatch):
    calls = []
    monkeypatch.setattr(commander.shutil, "which", lambda name: "/usr/bin/tmux")
    monkeypatch.setattr(commander, "session_exists", lambda name: True)
    monkeypatch.setattr(commander.subprocess, "run", lambda cmd, **k: calls.append(cmd))
    assert commander.spawn_tmux("bg-test") is True
    assert calls == []


def test_spawn_tmux_raises_when_command_fails(monkeypatch):
    monkeypatch.setattr(commander.shutil, "which", lambda name: "/usr/bin/tmux")
    monkeypatch.setattr(commander, "session_exists", lambda name: False)
    monkeypatch.setattr(commander.subprocess, "run", _raise_called_process_error)
    with pytest.raises(TmuxError, match="boom"):
        commander.spawn_tmux("bg-test")


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


def test_tell_tmux_raises_when_command_fails(monkeypatch):
    monkeypatch.setattr(commander, "session_exists", lambda name: True)
    monkeypatch.setattr(commander.subprocess, "run", _raise_called_process_error)
    with pytest.raises(TmuxError, match="send-keys gagal"):
        commander.tell_tmux("bg-test", "halo")