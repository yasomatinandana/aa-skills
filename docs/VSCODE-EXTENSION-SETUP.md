# Installing on the Claude Code VS Code extension (Windows)

How to make this repo's skills available inside the Claude Code **VS Code
extension**, as opposed to the standalone terminal CLI. This path exists
because the extension has a materially different feature set and no path to
a separate CLI install.

## Why this is a separate path

The VS Code extension (`anthropic.claude-code-*`) bundles its own copy of
the Claude Code engine — a `resources/native-binary` inside the extension
package. There is no user-installed `claude` CLI to configure, and none is
needed; this chat panel already is a full Claude Code session.

However, as of extension version `2.1.243`, **the `/plugin` command family
is not available** (`/plugin marketplace add`, `/plugin install`, etc. — the
extension replies `/plugin isn't available in this environment.`). This
repo's `.claude-plugin/marketplace.json` + `plugin.json` are valid and will
work with the terminal CLI or a future extension version, but they are inert
in this environment today. Do not delete them on that basis.

## The working mechanism: personal skills directory

Independent of the plugin system, Claude Code auto-discovers any folder
containing a `SKILL.md`:

- `~/.claude/skills/<name>/SKILL.md` — personal, loads in every project for
  this user.
- `<project>/.claude/skills/<name>/SKILL.md` — project-scoped.

This repo's `skills/engineering/`, `skills/productivity/`, and
`skills/pstack/` subfolders are each already shaped as one skill per
directory, so the fix is to get each skill folder to appear under
`~/.claude/skills/<name>/` without duplicating content.

## Link, don't copy — and don't trust `ln -s` on Windows

The instinct is to symlink each skill folder into `~/.claude/skills/`. Two
gotchas from Git Bash on Windows:

1. **True symlinks require elevation.** Without admin rights or Developer
   Mode enabled (Settings → Privacy & Security → For Developers), Windows
   won't create a real symlink for a directory.
2. **MSYS's `ln -s` fails silently into a full recursive copy.** Lacking the
   privilege for a real symlink, Git Bash's `ln -s` on a directory does not
   error — it silently copies the entire directory tree instead. `rm` on the
   result then errors `Is a directory` (a real symlink would unlink cleanly).
   This is easy to mistake for a working link; verify with `stat` (type
   should never read as a plain `directory` for something you intended as a
   link) or Windows' own `dir /a`, which labels genuine link points as
   `<JUNCTION>`/`<SYMLINK>` rather than `<DIR>`.

**Use NTFS junctions instead**, via `mklink /J`. Junctions don't require
admin rights or Developer Mode as long as source and target are on the same
drive (true here — both under `C:`). They're followed transparently by
normal file APIs, including whatever the extension uses to scan
`~/.claude/skills/`.

```bash
cmd //c "mklink /J C:\Users\<you>\.claude\skills\ask-matt C:\dev\aa-skills\skills\engineering\ask-matt"
```

Removing a junction later must go through `rmdir` (not `rm -rf`, which would
delete through the link and destroy the source content):

```bash
cmd //c "rmdir C:\Users\<you>\.claude\skills\ask-matt"
```

### Two argv-mangling traps when scripting this in Git Bash

- **Bare `/J` as its own argv token gets mistaken for a Unix path.** Git
  Bash's MSYS layer auto-translates arguments that look like absolute Unix
  paths before handing them to `cmd.exe`. An unquoted `/J` on its own
  qualifies and gets mangled, which surfaces as `mklink` reporting
  `Invalid switch` on what is actually your destination path (the shifted
  argument). Fix: pass the entire `mklink /J <dst> <src>` command as **one
  quoted string** to `cmd //c`, so `/J` is never a standalone argv token.
- **A trailing backslash right before a closing escaped quote breaks
  Windows argv parsing.** `"...\ask-matt\" "..."` — the lone `\` immediately
  before `"` is consumed per Windows' backslash-escaping rule (odd number of
  backslashes before a quote embeds a literal quote and does *not* close the
  string), so the quote you meant to close the argument doesn't. None of
  these paths contain spaces, so the simplest fix is to skip inner quoting
  entirely rather than trying to escape it correctly.

### Reusable loop

Run from anywhere, adjust the two path roots:

```bash
for src in /c/dev/aa-skills/skills/*/*/; do
  src="${src%/}"
  name=$(basename "$src")
  win_src=$(cygpath -w "$src")
  win_dst=$(cygpath -w "/c/Users/<you>/.claude/skills/$name")
  cmdline="mklink /J $win_dst $win_src"
  out=$(cmd //c "$cmdline" 2>&1)
  if [ $? -eq 0 ]; then echo "OK   $name"; else echo "FAIL $name -> $out"; fi
done
```

### Verifying

```bash
cmd //c "dir /a C:\Users\<you>\.claude\skills" | grep JUNCTION
cat ~/.claude/skills/why/SKILL.md | head -5   # content should resolve through the link
```

## Picking up new skills mid-session

A running Claude Code session has already loaded its skill list. New
junctions won't appear until you reload the window
(Ctrl+Shift+P → "Developer: Reload Window") or open a new session/tab.

## Net effect

Skills stay linked live to this repo — a `git pull` or local edit here is
immediately visible with no re-sync step. Linking under `~/.claude/skills/`
makes them available in every project for this user, not just one repo; use
`<project>/.claude/skills/` instead for a project-scoped install.
