import argparse
import sys

from .config import Config
from .graph import FactGraph


def cmd_setup(args) -> int:
    cfg = Config.load()
    fg = FactGraph(cfg.db_path)
    fg.add("Setup awal", "Graph berhasil dibuat", {"path": cfg.db_path})
    fg.close()
    print(f"[setup] graph siap: {cfg.db_path}")
    return 0


def cmd_status(args) -> int:
    cfg = Config.load()
    fg = FactGraph(cfg.db_path)
    for f in fg.list_titles():
        print(f"#{f['id']:>3} [{f['status']}] {f['title']}")
    fg.close()
    return 0


def cmd_add(args) -> int:
    cfg = Config.load()
    fg = FactGraph(cfg.db_path)
    fg.add(args.title, args.detail, {})
    fg.close()
    print(f"[add] task ditambahkan: {args.title}")
    return 0


def cmd_done(args) -> int:
    cfg = Config.load()
    fg = FactGraph(cfg.db_path)
    ids = {f["id"] for f in fg.list_titles()}
    if args.id not in ids:
        fg.close()
        print(f"[done] task #{args.id} tidak ditemukan", file=sys.stderr)
        return 1
    fg.update_status(args.id, "done")
    fg.close()
    print(f"[done] task #{args.id} selesai")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="builderguild")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("setup", help="inisialisasi graph")
    s.set_defaults(func=cmd_setup)

    s = sub.add_parser("status", help="tampilkan board")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("add", help="tambah task baru")
    s.add_argument("title")
    s.add_argument("--detail", default="")
    s.set_defaults(func=cmd_add)

    s = sub.add_parser("done", help="tandai task selesai")
    s.add_argument("id", type=int)
    s.set_defaults(func=cmd_done)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())