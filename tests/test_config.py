import pytest

from builderguild.config import Config, ConfigError


def test_config_defaults(monkeypatch):
    for key in ["BG_MAX_AGENTS", "BG_DB_PATH"]:
        monkeypatch.delenv(key, raising=False)
    cfg = Config.load()
    assert cfg.max_agents == 6
    assert cfg.db_path == "runs/graph.db"


def test_config_reads_env(monkeypatch):
    monkeypatch.setenv("BG_MAX_AGENTS", "3")
    assert Config.load().max_agents == 3


def test_config_rejects_non_numeric_agents(monkeypatch):
    monkeypatch.setenv("BG_MAX_AGENTS", "abc")
    with pytest.raises(ConfigError, match="BG_MAX_AGENTS"):
        Config.load()


def test_config_rejects_non_numeric_tokens(monkeypatch):
    monkeypatch.setenv("BG_MAX_TOKENS", "banyak")
    with pytest.raises(ConfigError, match="BG_MAX_TOKENS"):
        Config.load()