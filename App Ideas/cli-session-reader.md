# CLI Session Reader — App Idea

**Source:** Inbox (CLI Chats.md, captured from transcript)

## The Idea
A web UI for reading through Claude Code and Codex (OpenAI) session logs stored on the Mac. Tab interface at top lets you switch between Claude Code sessions and Codex sessions.

## Where Sessions Are Stored

**Claude Code:**
Sessions live at `~/.claude/projects/`. Each project is a subfolder named after the project path (with slashes replaced by dashes). Inside each project folder are `.jsonl` files — one per session — named by UUID. Each line is a JSON object representing one turn (user message, assistant message, tool use, tool result, etc.).

**Codex (OpenAI):**
Codex CLI stores sessions at `~/.codex/`. Sessions are stored as `.json` files, each containing the full conversation history for that session.

## UI Shape
- Two tabs: Claude Code | Codex
- File list on the left (sessions sorted by date, most recent first)
- Session viewer on the right — renders assistant/user turns in a clean chat layout
- Tool calls collapsible (show/hide)
- Search across sessions

## Build Notes
- Single-file HTML/JS app (no server needed — uses File System Access API or drag-and-drop to load session files)
- Or: a local server approach using a small Python/Node script that serves the files from the local filesystem
- The web File System Access API (`showDirectoryPicker()`) would let the user point it at their `~/.claude` or `~/.codex` folder directly in the browser with no server

## Priority
Medium — useful but not urgent. Good project for a rainy day build.
