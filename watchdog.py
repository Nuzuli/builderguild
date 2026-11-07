import time
import sys
from . import tmux_io
from .roles import ROLES

def ensure(role_name: str, ai_cmd: str = "bash") -> None:
    tmux_name = ROLES[role_name].tmux_name
    if not tmux_io.session_exists(tmux_name):
        tmux_io.spawn(tmux_name, ai_cmd)

def main(interval: int = 10) -> None:
    print("[watchdog] start (zero strategy)")
    try:
        while True:
            ensure("commander")
            ensure("scout")
            ensure("signalman")
            time.sleep(interval)
    except KeyboardInterrupt:
        sys.exit(0)