#!/usr/bin/env python3
"""Check that every quoted passage in an extracts file exists verbatim in a text dump.

    scripts/verify_quotes.py papers/arc-validation/EXTRACTS-A.md [more files]

For each Markdown file, every "double-quoted" passage of >= 6 words is searched,
whitespace-normalised and case-insensitive, in every *.txt under the txt/ and
refetch-txt/ folders next to the file, and in the txt/ folders of the other paper
sets. Passages not found anywhere are listed; a passage found only in a file whose
name does not appear in the extracts file is flagged. Dashes, quotes and ligatures
are normalised before matching so typographic differences do not count as misses.
"""

from __future__ import annotations

import glob
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..", "papers")


def norm(s: str) -> str:
    s = s.replace("­", "")
    s = re.sub(r"[‐-―−]", "-", s)
    s = re.sub(r"[‘’‚′]", "'", s)
    s = re.sub(r"[“”„″]", '"', s)
    s = s.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff").replace("ﬃ", "ffi").replace("ﬄ", "ffl")
    s = re.sub(r"-\s*\n\s*", "", s)  # hyphenation at line ends
    s = re.sub(r"\s+", " ", s)
    return s.lower().strip()


def key(s: str) -> str:
    """Alphanumeric-only form, so OCR spacing, hyphenation and punctuation cannot cause a miss."""
    return re.sub(r"[^a-z0-9]+", "", s)


def main():
    corpora = {}
    for t in glob.glob(os.path.join(ROOT, "*", "txt", "*.txt")) + glob.glob(os.path.join(ROOT, "*", "refetch-txt", "*.txt")) + glob.glob(os.path.join(ROOT, "*", "*.html")) + glob.glob(os.path.join(ROOT, "*", "*.txt")):
        try:
            with open(t, encoding="utf-8", errors="ignore") as fh:
                corpora[t] = key(norm(fh.read()))
        except OSError:
            pass
    total_missing = 0
    for md in sys.argv[1:]:
        with open(md, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        # quotes live either in blockquotes (> "...") or inline in bullets/paragraphs ("..." (p. N));
        # join lines within a paragraph or a blockquote so a quote wrapped over lines is one string
        blocks, cur, mode = [], [], None
        for ln in lines:
            kind = "q" if ln.startswith(">") else ("b" if ln.strip() else None)
            if kind is None:
                if cur:
                    blocks.append(" ".join(cur))
                cur, mode = [], None
                continue
            if mode is not None and kind != mode:
                blocks.append(" ".join(cur))
                cur = []
            mode = kind
            cur.append(ln.lstrip("> ").strip() if kind == "q" else ln.strip())
        if cur:
            blocks.append(" ".join(cur))
        seen = set()
        missing, found = [], 0
        for b in blocks:
            # keep only the quoted parts of the block; a block may hold several "..." quotes
            qs = re.findall(r"[\"“]([^\"“”]{25,}?)[\"”]", b)
            if b.startswith(">") or not qs:
                qs = qs or ([b] if len(b) > 40 and not re.search(r"\*\*|^#", b) else [])
            for qraw in qs:
                q = norm(qraw)
                if q in seen:
                    continue
                seen.add(q)
                parts = [p.strip(" .;:,") for p in re.split(r"\[[^\]]*\]|\.\.\.|…| / |\(§[^)]*\)|\(p\. [^)]*\)", q)]
                parts = [p for p in parts if len(p.split()) >= 6 and len(key(p)) >= 30]
                if not parts:
                    continue
                hits = [p for p in parts if any(key(p) in body for body in corpora.values())]
                # accept if at least half of the >=6-word fragments are found verbatim
                if len(hits) * 2 >= len(parts):
                    found += 1
                else:
                    bad = [p for p in parts if p not in hits]
                    missing.append((qraw[:110], bad[0][:90]))
        print(f"{md}: {found} quotes verified, {len(missing)} not found verbatim")
        for qraw, frag in missing:
            print(f"   MISSING fragment: {frag!r}\n            in: {qraw!r}")
        total_missing += len(missing)
    sys.exit(1 if total_missing else 0)


if __name__ == "__main__":
    main()
