---
type: tests
id: "Batch-009-Tests"
batch: "Batch-009"
---

# Acceptance tests

Candidate delivered. Every acceptance case is unexecuted.

- Tested commit: `22052a4f149acf6bcbfca99a57730b59a0ca0426` on `claude/batch-009`, pushed to `origin`.
- Environment or prerequisites: macOS 13 or later with Terminal, an authenticated `claude` executable (found in PATH, `~/.local/bin`, `~/.npm-global/bin`, `/opt/homebrew/bin` or `/usr/local/bin`), Apple developer tools, and a scratch project adopted with the kit that contains `agents/tools/krr-signal.py` and `agents/tools/configure-telegram.py` from this revision. Telegram must be configured for TEST-02 (see `agents/configure-telegram.md`). KRR needs the macOS Automation permission for Terminal, requested on first use (System Settings, Privacy & Security, Automation).
- Startup: from the repository root at the tested commit run `bash apps/krr/src/macos/build-app.sh "apps/krr/build/macos/krr-batch-009.app"` (already built at that path on the delivery checkout), then `open "apps/krr/build/macos/krr-batch-009.app"`. In the toolbar press **Claude Task**, choose the scratch project, enter the task and press **Start**. Claude is told to run `krr-signal.py waiting --id ID` before asking and `krr-signal.py resumed` when it continues. Copy `agents/tools/krr-signal.py` into the scratch project first.
- Technical evidence: `python3 agents/tools/test-krr-signal.py` (4 tests), `bash apps/krr/tests/macos/run-tests.sh` (Swift logic tests with a fake Terminal: silence, one alert per ID, repeated signal, resume, clarification, closed window, other windows untouched by construction, launcher quoting), `python3 agents/tools/test-kanban-board.py` (33 tests), `python3 agents/tools/test-telegram-setup.py`, board validation, `verify-approval Batch-009` and the app build all pass. Limit: the real Terminal AppleScript (`TerminalApp` in `claude-sessions.swift`), the form and a live Claude session could not be exercised by the agent because Automation permission needs the User; TEST-01 to TEST-05 are the first real run. Known unverified assumption: the window created by `do script` is `window 1` of Terminal.

| ID | Specifications | Action | Expected result | Verdict | Tested revision | Observation or evidence |
| --- | --- | --- | --- | --- | --- | --- |
| TEST-01 | SPEC-015 | Acceptance criterion 1: start the task from KR; run a deliberately slow command. | Terminal window minimized while Claude works; the slow command brings nothing forward and sends no alert. | OK | `22052a4` | User verdict OK on 2026-11-14. |
| TEST-02 | SPEC-015 | Criterion 2: Claude asks for CSV or JSON and waits; repeat the same signal. | The correct window is restored at normal size; one intervention alert; repeating the signal leaves the count at one. | OK | `22052a4` | User verdict OK on 2026-11-14. |
| TEST-03 | SPEC-015 | Criterion 3: ambiguous answer, clarification, then answer JSON. | Window stays visible while unresolved; once Claude resumes it minimizes; the export holds the expected record in JSON. | OK | `22052a4` | User verdict OK on 2026-11-14. |
| TEST-04 | SPEC-015 | Criterion 4: repeat with Telegram disabled or a simulated send failure. | The correct window still comes forward and accepts the answer. | OK | `22052a4` | User verdict OK on 2026-11-14. |
| TEST-05 | SPEC-015 | Criterion 5: second unrelated Terminal window; close the session while waiting. | Only the session window changes; KR shows the session ended and leaves the other window alone. | OK | `22052a4` | User verdict OK on 2026-11-14. |
| TEST-06 | SPEC-015 | Criterion 6: run an existing scheduled check. | It runs in the background with its existing permissions and opens no Terminal window. | OK | `22052a4` | User verdict OK on 2026-11-14. |

## Startup and actions by case

The full scenario of each case is the matching acceptance criterion of SPEC-015. Development Agent supplies the exact candidate revision, environment and startup instructions at delivery. Before each case is presented, Specification Agent writes its startup instructions, actions, expected result and stopping point here, following the guided acceptance procedure in `agents/roles/specification-agent.md`.
