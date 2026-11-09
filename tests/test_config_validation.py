import pytest

from builderguild.config import Config, ConfigError


def test_non_numeric_max_agents_raises_config_error(monkeypatch):
    monkeypatch.setenv("BG_MAX_AGENTS", "abc")
    with pytest.raises(ConfigError, match="BG_MAX_AGENTS"):
        Config.load()


def test_non_numeric_max_tokens_raises_config_error(monkeypatch):
    monkeypatch.setenv("BG_MAX_TOKENS", "banyak")
    with pytest.raises(ConfigError, match="BG_MAX_TOKENS"):
        Config.load()


def test_config_error_is_value_error():
    assert issubclass(ConfigError, ValueError)


def test_numeric_values_are_parsed(monkeypatch):
    monkeypatch.setenv("BG_MAX_AGENTS", "3")
    monkeypatch.setenv("BG_MAX_TOKENS", "1000")
    cfg = Config.load()
    assert cfg.max_agents == 3
    assert cfg.max_tokens == 1000