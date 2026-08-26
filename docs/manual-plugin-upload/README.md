# Manual plugin upload (claude.ai web)

How to package this repo as a `.zip` for the **Upload plugin** dialog in
Settings → Plugins on claude.ai. This path is separate from the GitHub-synced
marketplace flow (`marketplace.json` + `claude plugin validate`) — it's for
uploading a plugin archive by hand to a personal/org profile.

## Required zip structure

Per Anthropic's plugin docs, the archive must have `.claude-plugin/plugin.json`
either at the zip's top level, or one folder deep (both are accepted; deeper
nesting is not):

```
my-plugin.zip
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── skill-name/
        └── SKILL.md
```

`plugin.json` requires `name`, `description`, `version`, and `author.name`.
This repo's manifest lists skills as plugin-root-relative paths (e.g.
`./skills/engineering/ask-matt`), so **the plugin root has to be this repo's
root** — the zip must contain the whole repo (minus VCS/local-harness
clutter), not just the `skills/` subfolder.

Other constraints: zip must be under 50 MB (claude.ai upload limit; the
underlying plugin format allows up to 256 MiB), under 20,000 entries.

## Two mistakes that cause upload failures

1. **"Zip file contains path with invalid characters."**
   Building the zip with PowerShell's `Compress-Archive` (or
   `[System.IO.Compression.ZipFile]::CreateFromDirectory` under Windows
   PowerShell's .NET Framework runtime) bakes in backslash (`\`) path
   separators, e.g. `engineering\ask-matt\SKILL.md`. The zip spec requires
   forward slashes (`/`) in entry names — Windows tooling doesn't normalize
   this automatically. `build-plugin-zip.ps1` below writes entries manually
   with forward slashes to avoid it.

2. **"Zip must contain a .claude-plugin/plugin.json file or a top-level
   SKILL.md."**
   Zipping only the `skills/` folder (so the archive's root is
   `engineering/`, `productivity/`, `pstack/`) omits `.claude-plugin/`
   entirely. The zip has to start at the repo root, not inside `skills/`.

## Usage

From the repo root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File docs/manual-plugin-upload/build-plugin-zip.ps1
```

This writes `aa-skills-claude-skills.zip` to `C:/dev/` (one level above the
repo), excluding `.git` and any gitignored local-harness directories
(`.hermes/`, `.claude/`, `.codex/`, `.cursor/`, `node_modules/`).

Then in claude.ai: Settings → Plugins → Add → Upload a file → select the zip.

## Verifying before upload

Spot-check that entries use forward slashes and `.claude-plugin/plugin.json`
is at (or one folder below) the archive root:

```bash
unzip -l aa-skills-claude-skills.zip | head -20
unzip -l aa-skills-claude-skills.zip | grep '\\\\'   # should print nothing
```

If you bump `plugin.json`'s `version`, re-run the build script before
re-uploading — claude.ai uses the version (or the archive's sha256 if
unversioned) to decide whether an upload is a new revision.
