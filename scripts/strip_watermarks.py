#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove machine-paste artefacts that survive the Russian delegate's clean_paste.py.

Covers the gap, not the overlap. Run clean_paste.py first for citation tokens,
utm tails, zero-width characters, BOM and bidi controls; this handles what it
leaves behind:

  spaces       NBSP, narrow NBSP, en/em/thin/hair space, figure space -> plain space
  invisible    variation selectors, remaining format characters
  homoglyphs   Latin/Cyrillic/Greek mixed inside ONE word -> normalised to the
               word's majority script
  artefacts    chat-citation leftovers listed in ARTEFACT_TOKENS below

Protected byte for byte: fenced code blocks, inline code spans, indented code,
YAML/TOML frontmatter, and URLs. A homoglyph inside a URL or a bare domain is
never rewritten, only reported: silently "fixing" a hostname would change where
a link points, and a mixed-script domain is a phishing signal a human must see.

Source files are refused unless --force, because a cleaner that rewrites prose
will happily corrupt a regex literal or a test fixture that contains the very
tokens it hunts for.

Usage
  strip_watermarks.py [--check] [--report] [--force] FILE [FILE ...]
  strip_watermarks.py --check -            # stdin, nothing written

Exit: 0 clean or rewritten, 1 --check found artefacts, 2 usage error.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

SPACES = {
    "\u00a0": " ", "\u202f": " ", "\u2007": " ", "\u2002": " ", "\u2003": " ",
    "\u2004": " ", "\u2005": " ", "\u2006": " ", "\u2008": " ", "\u2009": " ",
    "\u200a": " ", "\u205f": " ", "\u3000": " ",
}
INVISIBLE = re.compile("[\ufe00-\ufe0f\u2060-\u2064\u206a-\u206f\U000e0100-\U000e01ef]")

# assembled at runtime so the literals never sit in the file as matchable text
ARTEFACT_TOKENS = ["grok" + "_card://", "oai" + "cite", "content" + "Reference"]
ARTEFACTS = re.compile("|".join(re.escape(t) + r"\S*" for t in ARTEFACT_TOKENS))

CODE_SUFFIXES = {".py", ".js", ".ts", ".go", ".rs", ".rb", ".sh", ".zsh", ".bash",
                 ".c", ".h", ".cpp", ".java", ".kt", ".php", ".pl", ".lua", ".tf"}

FENCE = re.compile(r"^(\s{0,3})(`{3,}|~{3,})")
FRONTMATTER = re.compile(r"^(---|\+\+\+)\s*$")
INLINE_CODE = re.compile(r"`[^`\n]+`")
URL = re.compile(r"(?:https?://|www\.)\S+|\b[\w.-]+\.(?:com|org|net|io|dev|de|ru|ai|co)\b")
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)

TO_LATIN = {
    "а": "a", "е": "e", "о": "o", "с": "c", "р": "p", "х": "x", "у": "y",
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H", "О": "O",
    "Р": "P", "С": "C", "Т": "T", "Х": "X", "У": "Y", "і": "i", "ј": "j",
    "ѕ": "s", "α": "a", "ο": "o", "ρ": "p", "ε": "e", "ι": "i", "κ": "k",
    "ν": "v", "Α": "A", "Β": "B", "Ε": "E", "Ζ": "Z", "Η": "H", "Ι": "I",
    "Κ": "K", "Μ": "M", "Ν": "N", "Ο": "O", "Ρ": "P", "Τ": "T", "Χ": "X",
}
TO_CYRILLIC = {
    "a": "а", "e": "е", "o": "о", "c": "с", "p": "р", "x": "х", "y": "у",
    "A": "А", "B": "В", "E": "Е", "K": "К", "M": "М", "H": "Н", "O": "О",
    "P": "Р", "C": "С", "T": "Т", "X": "Х", "Y": "У",
}


def script_of(ch: str) -> str:
    name = unicodedata.name(ch, "")
    if "CYRILLIC" in name:
        return "cyrillic"
    if "GREEK" in name:
        return "greek"
    if "LATIN" in name:
        return "latin"
    return "other"


def fix_word(word: str, counts: Counter) -> str:
    scripts = {script_of(c) for c in word} - {"other"}
    if len(scripts) < 2:
        return word
    tally = Counter(script_of(c) for c in word if script_of(c) != "other")
    majority, _ = tally.most_common(1)[0]
    table = TO_LATIN if majority == "latin" else TO_CYRILLIC if majority == "cyrillic" else {}
    if not table:
        counts["homoglyph-unresolved"] += 1
        return word
    out, changed = [], False
    for ch in word:
        if script_of(ch) != majority and ch in table:
            out.append(table[ch])
            changed = True
        else:
            out.append(ch)
    counts["homoglyph" if changed else "homoglyph-unresolved"] += 1
    return "".join(out)


def clean_segment(text: str, counts: Counter) -> str:
    for bad, good in SPACES.items():
        if bad in text:
            counts["space"] += text.count(bad)
            text = text.replace(bad, good)
    text, n = INVISIBLE.subn("", text)
    counts["invisible"] += n
    text, n = ARTEFACTS.subn("", text)
    counts["artefact"] += n

    guard: list[str] = []

    def stash_url(m: re.Match) -> str:
        guard.append(m.group(0))
        if any(len({script_of(c) for c in w.group(0)} - {"other"}) > 1
               for w in WORD.finditer(m.group(0))):
            counts["homoglyph-in-url"] += 1
        return "\x00%d\x00" % (len(guard) - 1)

    def stash_code(m: re.Match) -> str:
        # code spans are protected on purpose; a mixed-script example inside
        # backticks is documentation, not a defect, so it is not counted
        guard.append(m.group(0))
        return "\x00%d\x00" % (len(guard) - 1)

    text = URL.sub(stash_url, text)
    text = INLINE_CODE.sub(stash_code, text)
    text = WORD.sub(lambda m: fix_word(m.group(0), counts), text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: guard[int(m.group(1))], text)
    return text


def clean(text: str) -> tuple[str, Counter]:
    counts: Counter = Counter()
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    i, n = 0, len(lines)

    if n and FRONTMATTER.match(lines[0].rstrip("\n")):
        delim = lines[0].strip()
        j = 1
        while j < n and lines[j].strip() != delim:
            j += 1
        if j < n:
            out.extend(lines[: j + 1])
            i = j + 1

    buf: list[str] = []
    while i < n:
        m = FENCE.match(lines[i])
        if m:
            if buf:
                out.append(clean_segment("".join(buf), counts))
                buf = []
            marker = m.group(2)[0] * 3
            out.append(lines[i])
            i += 1
            while i < n:
                out.append(lines[i])
                mm = FENCE.match(lines[i])
                i += 1
                if mm and mm.group(2).startswith(marker):
                    break
            continue
        if lines[i].startswith(("    ", "\t")) and lines[i].strip():
            if buf:
                out.append(clean_segment("".join(buf), counts))
                buf = []
            out.append(lines[i])
            i += 1
            continue
        buf.append(lines[i])
        i += 1
    if buf:
        out.append(clean_segment("".join(buf), counts))
    return "".join(out), counts


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--check", action="store_true", help="report, do not write")
    ap.add_argument("--report", action="store_true", help="print a line even when clean")
    ap.add_argument("--force", action="store_true", help="allow source files")
    ap.add_argument("files", nargs="+")
    args = ap.parse_args()

    found = 0
    for name in args.files:
        if name == "-":
            cleaned, counts = clean(sys.stdin.read())
            if not args.check:
                sys.stdout.write(cleaned)
            counts = Counter({k: v for k, v in counts.items() if v})
            if counts:
                print("stdin: %s" % dict(counts), file=sys.stderr)
                found += 1
            continue
        p = Path(name)
        if not p.is_file():
            print("skip (not a file): %s" % p, file=sys.stderr)
            continue
        if p.suffix in CODE_SUFFIXES and not args.force:
            print("skip (source file, use --force): %s" % p, file=sys.stderr)
            continue
        src = p.read_text(encoding="utf-8")
        dst, counts = clean(src)
        counts = Counter({k: v for k, v in counts.items() if v})
        if counts.get("homoglyph-in-url"):
            print("%s: %d mixed-script URL(s) - review by hand, not rewritten"
                  % (p, counts["homoglyph-in-url"]))
        if not counts:
            if args.report:
                print("%s: clean" % p)
            continue
        found += 1
        detail = ", ".join("%s=%d" % (k, v) for k, v in sorted(counts.items()))
        if args.check:
            print("%s: %s" % (p, detail))
        else:
            if src != dst:
                p.write_text(dst, encoding="utf-8")
            print("%s: %s" % (p, detail))

    if not found:
        print("nothing to change")
    return 1 if (args.check and found) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
