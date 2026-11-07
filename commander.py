import time
from .config import Config
from .graph import FactGraph
from . import roles

def plan(fg: FactGraph) -> list[dict]:
    open_facts = fg.list_titles(status="open")
    return sorted(open_facts, key=lambda f: len(f["title"]))

def run(cfg: Config, interval: int = 30) -> None:
    fg = FactGraph(cfg.db_path)
    print(f"[commander] start; db={cfg.db_path}")
    try:
        while True:
            tasks = plan(fg)
            for t in tasks[: cfg.max_agents]:
                role = "soldier" if len(t["title"]) < 60 else "general"
                fg.update_status(t["id"], "in_progress", owner=role)
                roles.dispatch(role, f"[fact#{t['id']}] {t['title']}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("[commander] stop.")
    finally:
        fg.close()