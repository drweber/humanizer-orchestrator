#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collapse redundant blank lines without touching code or frontmatter.

Targets
  md      max one blank line between blocks (the Markdown paragraph separator stays)
  plain   paragraphs separated by a single newline, no blank lines
  commit  subject line, exactly one blank line, then body with single newlines

Protected byte for byte: fenced code blocks, indented code, and YAML/TOML
frontmatter delimited by --- or +++ at the very start of the file. One blank
line is kept before an opening fence and after a closing fence or frontmatter,
because markdownlint MD031 and MD022 require it.

Usage
  normalize_whitespace.py [--target md|plain|commit] [--check] FILE [FILE ...]
  cat x.md | normalize_whitespace.py --target md -

Exit: 0 clean or rewritten, 1 --check found changes, 2 usage error.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FENCE = re.compile(r"^(\s{0,3})(`{3,}|~{3,})(.*)$")
FRONTMATTER = re.compile(r"^(---|\+\+\+)\s*$")
TRAILING = re.compile(r"[ \t]+$")
HARD_BREAK = re.compile(r"\S {2}$")


def split_protected(lines):
    out, i, n = [], 0, len(lines)
    if n and FRONTMATTER.match(lines[0]):
        delim = lines[0].strip()
        j = 1
        while j < n and lines[j].strip() != delim:
            j += 1
        if j < n:
            out.append(("front", lines[: j + 1]))
            i = j + 1
    buf = []
    while i < n:
        m = FENCE.match(lines[i])
        if m:
            if buf:
                out.append(("text", buf))
                buf = []
            marker = m.group(2)[0] * 3
            block = [lines[i]]
            i += 1
            while i < n:
                block.append(lines[i])
                mm = FENCE.match(lines[i])
                if mm and mm.group(2).startswith(marker) and not mm.group(3).strip():
                    i += 1
                    break
                i += 1
            out.append(("code", block))
            continue
        buf.append(lines[i])
        i += 1
    if buf:
        out.append(("text", buf))
    return out


def normalize_text(lines, target, allow_leading_blank=False):
    cleaned = [ln if HARD_BREAK.search(ln) else TRAILING.sub("", ln) for ln in lines]
    if target == "plain":
        return [ln for ln in cleaned if ln.strip()]
    out, blank_run, leading_used = [], 0, False
    for ln in cleaned:
        if not ln.strip():
            blank_run += 1
            if blank_run > 1:
                continue
            if not out:
                if allow_leading_blank and not leading_used:
                    leading_used = True
                    out.append("")
                continue
            out.append("")
        else:
            blank_run = 0
            out.append(ln)
    return out


def normalize(text, target):
    pieces = split_protected(text.splitlines())
    result, prev_protected = [], False
    for kind, block in pieces:
        if kind in ("code", "front"):
            if kind == "code" and result and result[-1].strip() and target != "plain":
                result.append("")
            result.extend(block)
            prev_protected = True
        else:
            result.extend(normalize_text(
                block, target, allow_leading_blank=prev_protected and target != "plain"))
            prev_protected = False
    while result and not result[-1].strip():
        result.pop()
    if target == "commit" and result:
        subject = result[0].rstrip()
        body = [ln for ln in result[1:] if ln.strip()]
        result = [subject] + ([""] + body if body else [])
    return "\n".join(result) + "\n" if result else ""


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--target", choices=("md", "plain", "commit"), default="md")
    ap.add_argument("--check", action="store_true", help="report, do not write")
    ap.add_argument("files", nargs="+")
    args = ap.parse_args()

    changed = 0
    for name in args.files:
        if name == "-":
            sys.stdout.write(normalize(sys.stdin.read(), args.target))
            continue
        p = Path(name)
        if not p.is_file():
            print("skip (not a file): %s" % p, file=sys.stderr)
            continue
        src = p.read_text(encoding="utf-8")
        dst = normalize(src, args.target)
        if src == dst:
            continue
        changed += 1
        removed = len(src.splitlines()) - len(dst.splitlines())
        if args.check:
            print("%s: %d line(s) would be removed" % (p, removed))
        else:
            p.write_text(dst, encoding="utf-8")
            print("%s: %d line(s) removed" % (p, removed))
    if not changed:
        print("nothing to change")
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
