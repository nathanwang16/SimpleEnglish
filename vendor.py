#!/usr/bin/env python3
"""Copy the simple-english skill into a repository so that it loads from git.

Usage: python3 vendor.py DEST_SKILLS_DIR
  DEST_SKILLS_DIR is the directory that the repository's .claude/skills
  resolves to, for example unicorn-baseline/skills or unicorn-trade/.claude/skills.

It writes DEST_SKILLS_DIR/simple-english/ with SKILL.md and hooks/ (lint_hook.py,
ste_lint.py, slop.tsv). The SKILL.md hooks call
$CLAUDE_PROJECT_DIR/.claude/skills/simple-english/hooks/lint_hook.py, so the
repository must reach the skill through .claude/skills.
"""
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent
FILES = {
    "SKILL.md": ROOT / "skills/simple-english/SKILL.md",
    "hooks/lint_hook.py": ROOT / "src/hooks/lint_hook.py",
    "hooks/ste_lint.py": ROOT / "evals/ste_lint.py",
    "hooks/slop.tsv": ROOT / "evals/slop.tsv",
}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    dest = pathlib.Path(sys.argv[1]) / "simple-english"
    for name, src in FILES.items():
        out = dest / name
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out)
        print(out)


if __name__ == "__main__":
    main()
