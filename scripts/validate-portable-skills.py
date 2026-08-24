#!/usr/bin/env python3
"""Validate aa-skills provenance, links, frontmatter, and portability markers."""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
for skill in sorted((ROOT / "skills").rglob("SKILL.md")):
    text = skill.read_text(encoding="utf-8")
    rel = skill.relative_to(ROOT)
    if not text.startswith("---"):
        errors.append(f"{rel}: missing YAML frontmatter")
    if "name:" not in text or "description:" not in text:
        errors.append(f"{rel}: missing name or description")
    if len(text) > 100_000:
        errors.append(f"{rel}: exceeds 100000 bytes")
    for token in ("~/.cursor", "AskQuestion", "subagent_type", "Graphite"):
        if token in text and "skills/pstack/" not in str(rel):
            errors.append(f"{rel}: harness-specific token {token!r}; move it to an adapter or mark the skill explicitly")
    for href in re.findall(r"\]\(([^)]+)\)", text):
        if href.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if href == "link" or "<" in href or ">" in href:
            continue
        candidate = (skill.parent / href).resolve()
        if not candidate.exists():
            errors.append(f"{rel}: broken link {href}")
if not (ROOT / "docs/UPSTREAM-ATTRIBUTION.md").exists():
    errors.append("missing docs/UPSTREAM-ATTRIBUTION.md")
for license_name in ("pstack-LICENSE", "mattpocock-LICENSE"):
    if not (ROOT / "upstream" / license_name).exists():
        errors.append(f"missing upstream/{license_name}")
if errors:
    print("VALIDATION FAILED")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print(f"VALIDATION PASSED: {len(list((ROOT / 'skills').rglob('SKILL.md')))} skill files")
