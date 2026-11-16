from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from robot_corpus.control_plane import Application, run, verify


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog='robot_corpus', description='工业机器人具身数据采集编排中心')
    commands = root.add_subparsers(dest="command", required=True)
    execute = commands.add_parser("run")
    execute.add_argument("--fixture", required=True)
    execute.add_argument("--database", required=True)
    execute.add_argument("--output", required=True)
    check = commands.add_parser("verify")
    check.add_argument("--database", required=True)
    check.add_argument("--output", required=True)
    inspect = commands.add_parser("inspect")
    inspect.add_argument("--database", required=True)
    coverage = commands.add_parser("coverage")
    coverage.add_argument("--database", required=True)
    reevaluate = commands.add_parser("reevaluate")
    reevaluate.add_argument("--database", required=True)
    reevaluate.add_argument("--session", action="append", dest="sessions")
    review = commands.add_parser("review")
    review.add_argument("--database", required=True)
    review.add_argument("--dataset", required=True)
    return root


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "run":
        result = run(args.fixture, args.database, args.output)
    elif args.command == "verify":
        result = verify(args.database, args.output)
    elif args.command == "coverage":
        result = Application(args.database).coverage_report()
    elif args.command == "reevaluate":
        result = Application(args.database).reevaluate(args.sessions)
    elif args.command == "review":
        result = Application(args.database).review_dataset(args.dataset)
    else:
        result = Application(args.database).inspect()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
