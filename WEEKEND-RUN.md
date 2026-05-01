# Weekend Run — Kickoff Instructions

**Goal:** Build 10 new South Fork Apps autonomously over the weekend. Agent works through todo.md, validates each app, checks it off, moves on.

**Files:**
- `spec.md` — all requirements the agent follows
- `todo.md` — 10 apps, checkbox format (agent checks off as it goes)
- `tests/validate.sh` — run after each app to verify it's correct

---

## Option A — Gemini CLI (recommended, free, no rate limits)

```bash
cd "/Users/tuckerchastain/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tucker Chastain/77_South Fork Apps"
gemini
```

Paste this prompt:
```
Read spec.md and todo.md in this directory. Work through each unchecked item in todo.md one at a time. For each app: build the folder and files exactly as spec.md requires, run bash tests/validate.sh [app-folder-name] to verify, then check off the item in todo.md. Do not ask for confirmation. Continue until all items are checked off.
```

---

## Option B — Claude Code (familiar, will pause at rate limit — auto-resumes)

Open a new terminal tab (not this Cog session):

```bash
cd "/Users/tuckerchastain/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tucker Chastain/77_South Fork Apps"
claude --dangerously-skip-permissions
```

Paste the same prompt above. If Claude hits a rate limit, it will stop. Just run the same command again — it reads todo.md and skips already-checked items automatically.

---

## Option C — Ollama / cog-local (slowest, never stops)

```bash
cd "/Users/tuckerchastain/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tucker Chastain/77_South Fork Apps"
cog-local
```

Same prompt. Use this if both A and B fail.

---

## Run in tmux (so it keeps going when you close the lid)

```bash
tmux new-session -s weekend-run
# then run Option A or B inside that session
# detach with: Cmd+B then D
# reattach later with: tmux attach -t weekend-run
```

---

## Check Progress Anytime

```bash
grep -c "\[x\]" "/Users/tuckerchastain/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tucker Chastain/77_South Fork Apps/todo.md"
```

Returns number of completed apps (out of 10).

Or just open todo.md in Obsidian and look at the checkboxes.

---

## When It's Done

1. Open todo.md — all 10 should be checked
2. Run `bash tests/validate.sh` (no argument) to verify all apps pass
3. Tell Cog "weekend run done" and Cog will add the new app cards to southforkapps.com index.html

---

## Adding Apps to southforkapps.com After the Run

Tucker does this manually (or asks Cog). Each app needs a card added to the main `index.html`. The agent does NOT touch southforkapps.com during the run — that's deliberate.
