#!/usr/bin/env python3
"""Advisory writing checks for Claude Code hooks. Never blocks.

PostToolUse (Write|Edit on a .md file): lint the text the tool wrote (the
whole content for Write, the new text for Edit) with evals/ste_lint.py and,
when it has violations, print the offending text and line number for
each hit (capped at MAX_HOOK_HITS) to stderr and exit 2 so the model sees
it. Exit 2 on PostToolUse is advisory: the tool already ran. Agent-internal
Markdown, such as memory files under the Claude configuration directory, is
skipped. The writing rules do not govern it, and a summary of its
violations only spends tokens. Set SIMPLE_ENGLISH_LINT_EXCLUDE to skip more
paths.

Stop and SubagentStop: read `last_assistant_message`, check the reply
register (no em-dashes, no bold after the headline line), and return a systemMessage only when the reply
breaks it. Always exit 0, so the session never loops.
"""
import fnmatch
import json
import os
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "evals"))
sys.path.insert(0, str(HERE))  # a vendored copy keeps ste_lint.py beside this file

MAX_HOOK_HITS = 12
CLAUDE_DIR = ".claude"
OPENERS = re.compile(r"^\s*(certainly|great question|you're absolutely right|sure[,!]|absolutely[,!])", re.I)
CLOSERS = re.compile(r"(i hope this helps|let me know if|feel free to)", re.I)


def load_linter():
    try:
        import ste_lint  # noqa: WPS433
        return ste_lint
    except Exception:  # noqa: BLE001
        return None


def strip_code(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    return re.sub(r"`[^`]*`", " ", text)


def absolute(path, cwd=None):
    """Make the path absolute. The harness can send it relative to the session directory."""
    return pathlib.Path(cwd or ".", pathlib.Path(path).expanduser()).absolute()


def variants(path):
    """The path as written and the path with symlinks resolved. An exclusion matches either form.

    A symlink hides a directory name in both directions. `notes.md` can point into `.claude`,
    and `.claude` itself can point at a dotfiles repository. Both forms must miss for the
    file to reach the linter.
    """
    return {pathlib.Path(os.path.normpath(path)), path.resolve()}


def excluded(target):
    """True for agent-internal Markdown and for the paths the user excludes."""
    config_dirs = variants(absolute(os.environ.get("CLAUDE_CONFIG_DIR") or f"~/{CLAUDE_DIR}"))
    raw = os.environ.get("SIMPLE_ENGLISH_LINT_EXCLUDE", "").split(os.pathsep)
    patterns = [os.path.expanduser(p) for p in raw if p]
    for form in variants(target):
        if CLAUDE_DIR in form.parts or any(form.is_relative_to(d) for d in config_dirs):
            return True
        if any(fnmatch.fnmatch(str(form), p) for p in patterns):
            return True
    return False


def written_text(event):
    """The text the tool wrote: the whole file for Write, the new text only for Edit.

    Linting the whole file after an Edit would ask the model to rewrite lines
    it did not write, which can belong to another session or to the owner.
    """
    tool_input = event.get("tool_input") or {}
    if event.get("tool_name") == "Edit":
        return tool_input.get("new_string") or ""
    return tool_input.get("content") or ""


def post_tool_use(event):
    path = (event.get("tool_input") or {}).get("file_path") or ""
    if not path.endswith(".md"):
        return 0
    target = absolute(path, event.get("cwd"))
    if excluded(target):
        return 0
    lint = load_linter()
    if lint is None:
        return 0
    text = written_text(event)
    if not text.strip():
        return 0
    report = lint.lint(text, "descriptive")
    if not report["violations_total"]:
        return 0
    detail = lint.lint_detail(text, "descriptive")
    lines = [f"simple-english: the text you wrote to {target.name} has {report['violations_total']} STE violations."]
    for h in detail[:MAX_HOOK_HITS]:
        lines.append(f"  line {h['line']} of that text, {h['category']}: {h['text']}")
    if len(detail) > MAX_HOOK_HITS:
        lines.append(f"  and {len(detail) - MAX_HOOK_HITS} more hit(s).")
    lines.append("Fix these hits in the text you just wrote, keep every word that docs/vocabulary.md gives, then continue.")
    sys.stderr.write("\n".join(lines) + "\n")
    return 2


def without_headline(reply):
    """The reply less its first non-empty line. The headline can be bold."""
    lines = reply.lstrip("\n").split("\n", 1)
    return lines[1] if len(lines) > 1 else ""


def stop(event):
    reply = event.get("last_assistant_message") or ""
    body = without_headline(reply)
    problems = []
    lint = load_linter()
    if lint is not None:
        dashes = lint.reader_check(reply)["counts"]["em_dash"]
        if dashes:
            problems.append(f"{dashes} em-dash(es)")
        bold = lint.reader_check(body)["counts"]["bold_spans"]
        if bold:
            problems.append(f"{bold} bold span(s) after the headline")
        slop = lint.lint(strip_code(reply), "descriptive")["violations"].get("slop_word", 0)
        if slop:
            problems.append(f"{slop} slop word(s)")
    if OPENERS.search(reply):
        problems.append("a filler opener")
    if CLOSERS.search(reply):
        problems.append("a filler closer")
    if problems:
        print(json.dumps({"systemMessage": "simple-english reply check: " + "; ".join(problems) + "."}))
    return 0


def main():
    try:
        event = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        return 0
    try:
        name = event.get("hook_event_name", "")
        if name == "PostToolUse":
            return post_tool_use(event)
        if name in ("Stop", "SubagentStop"):
            return stop(event)
    except Exception:  # noqa: BLE001  advisory hook: a crash must never block or loop the session
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
