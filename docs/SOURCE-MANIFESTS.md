# Source manifests

The active source manifests are upstream-specific and are not used as aa-skills manifests.

- pstack Cursor manifest: `https://github.com/cursor/plugins/blob/main/pstack/.cursor-plugin/plugin.json`
- Matt Pocock Claude manifest: `https://github.com/mattpocock/skills/blob/main/.claude-plugin/plugin.json`
- Superpowers Claude manifest: `https://github.com/obra/superpowers/blob/main/.claude-plugin/plugin.json` (name `superpowers`, version 6.3.0 at revision `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`)

The adapters intentionally avoid copying these manifests unchanged because their paths and invocation semantics are harness-specific.
