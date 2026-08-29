#!/usr/bin/env python3
"""Validate aa-skills provenance, links, frontmatter, portability markers,
manifest consistency, and skill-name uniqueness."""
from pathlib import Path
import json
import re
import sys

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

# Link check across all markdown under skills/ (references and prompts link too).
# Code-fenced content is illustrative example output, not real links — strip it first.
def _strip_fences(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)

for md in sorted((ROOT / "skills").rglob("*.md")):
    if md.name == "SKILL.md":
        continue
    text = _strip_fences(md.read_text(encoding="utf-8"))
    rel = md.relative_to(ROOT)
    for href in re.findall(r"\]\(([^)]+)\)", text):
        if href.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if href == "link" or href == "url" or "<" in href or ">" in href:
            continue
        candidate = (md.parent / href.split("#")[0].strip()).resolve()
        if not candidate.exists():
            errors.append(f"{rel}: broken link {href}")

# Manifest consistency: every listed skill dir exists and contains SKILL.md.
for adapter in ("claude-code", "hermes-agent"):
    manifest = ROOT / "adapters" / adapter / "plugin.json"
    if not manifest.exists():
        errors.append(f"missing {manifest.relative_to(ROOT)}")
        continue
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{manifest.relative_to(ROOT)}: invalid JSON ({exc})")
        continue
    for entry in data.get("skills", []):
        skill_md = (manifest.parent / entry / "SKILL.md").resolve()
        if not skill_md.exists():
            errors.append(f"{manifest.relative_to(ROOT)}: listed skill has no SKILL.md: {entry}")

# Codex convention: every skill with a SKILL.md carries agents/openai.yaml.
for skill_md in (ROOT / "skills").rglob("SKILL.md"):
    if not (skill_md.parent / "agents" / "openai.yaml").exists():
        errors.append(f"{skill_md.relative_to(ROOT)}: missing agents/openai.yaml (Codex metadata)")

# Skill-name uniqueness: frontmatter names must not collide across bundles.
seen = {}
for skill_md in (ROOT / "skills").rglob("SKILL.md"):
    text = skill_md.read_text(encoding="utf-8")
    m = re.search(r"^name:\s*(.+?)\s*$", text, re.MULTILINE)
    if not m:
        continue
    name = m.group(1).strip().strip("'\"")
    rel = str(skill_md.relative_to(ROOT))
    if name in seen:
        errors.append(f"duplicate skill name {name!r}: {seen[name]} and {rel}")
    else:
        seen[name] = rel

# Secret scan over imported skill content (heuristics; provenance docs excluded).
SECRET_RE = re.compile(
    r"(-----BEGIN [A-Z ]*PRIVATE KEY-----|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|"
    r"xox[baprs]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16})"
)
for md in (ROOT / "skills").rglob("*"):
    if md.suffix not in (".md", ".yaml", ".sh", ".ts", ".js"):
        continue
    text = md.read_text(encoding="utf-8", errors="ignore")
    if SECRET_RE.search(text):
        errors.append(f"{md.relative_to(ROOT)}: possible credential material — review before distributing")

if not (ROOT / "docs/UPSTREAM-ATTRIBUTION.md").exists():
    errors.append("missing docs/UPSTREAM-ATTRIBUTION.md")
for license_name in ("pstack-LICENSE", "mattpocock-LICENSE", "superpowers-LICENSE"):
    if not (ROOT / "upstream" / license_name).exists():
        errors.append(f"missing upstream/{license_name}")

if errors:
    print("VALIDATION FAILED")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
skill_count = len(list((ROOT / 'skills').rglob('SKILL.md')))
print(f"VALIDATION PASSED: {skill_count} skill files, names unique, manifests consistent")
