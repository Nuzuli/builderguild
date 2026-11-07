import os
from dataclasses import dataclass

def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)

@dataclass
class Config:
    commander_model: str = _env("BG_COMMANDER_MODEL", "claude-sonnet-4-5")
    soldier_model: str = _env("BG_SOLDIER_MODEL", "claude-haiku-4-5")
    max_tokens: int = int(_env("BG_MAX_TOKENS", "200000"))
    max_agents: int = int(_env("BG_MAX_AGENTS", "6"))
    db_path: str = _env("BG_DB_PATH", "runs/graph.db")
    repo_path: str = _env("BG_REPO_PATH", ".")

    @classmethod
    def load(cls) -> "Config":
        return cls()

def model_for(role: str, cfg: Config) -> str:
    if role in ("commander", "general"):
        return cfg.commander_model
    return cfg.soldier_model