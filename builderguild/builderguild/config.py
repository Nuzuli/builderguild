import os
from dataclasses import dataclass, field


class ConfigError(ValueError):
    """Dilempar saat nilai konfigurasi dari environment tidak valid."""


def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def _env_int(key: str, default: str, minimum: int | None = None) -> int:
    raw = _env(key, default)
    try:
        value = int(raw)
    except ValueError:
        raise ConfigError(f"{key} harus berupa angka bulat, dapat: {raw!r}") from None
    if minimum is not None and value < minimum:
        raise ConfigError(f"{key} minimal {minimum}, dapat: {value}")
    return value


@dataclass
class Config:
    commander_model: str = field(
        default_factory=lambda: _env("BG_COMMANDER_MODEL", "claude-sonnet-4-5")
    )
    soldier_model: str = field(
        default_factory=lambda: _env("BG_SOLDIER_MODEL", "claude-haiku-4-5")
    )
    max_tokens: int = field(
        default_factory=lambda: _env_int("BG_MAX_TOKENS", "200000", minimum=1)
    )
    max_agents: int = field(
        default_factory=lambda: _env_int("BG_MAX_AGENTS", "6", minimum=1)
    )
    db_path: str = field(default_factory=lambda: _env("BG_DB_PATH", "runs/graph.db"))
    repo_path: str = field(default_factory=lambda: _env("BG_REPO_PATH", "."))

    @classmethod
    def load(cls) -> "Config":
        return cls()