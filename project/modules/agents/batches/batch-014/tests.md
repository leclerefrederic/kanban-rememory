---
type: tests
id: "Batch-014-Tests"
batch: "Batch-014"
---

# Acceptance tests

- Tested commit: `f18e413db9ae6d61f8e84e4d6e91b1a682e274a8` (corrected candidate; previous observations retain their exact revisions below).
- Environment or prerequisites: Start a fresh chat in `/private/tmp/kr-batch014-uat.vHwJCr/project` as KR Orchestrator. The clean checkout is at the exact tested commit. Its only Git remote is the local fixture origin. Use disposable Cards and Batches and simulate notification delivery. Disable real notifications for the entire fixture session.
- Technical evidence: Candidate diff, Kanban validation and installed skill consistency checks passed. Walked through the four scenarios against the instructions: an initial visible line precedes delegation; a long wait permits a short update after about a minute; a blocker or required decision receives context; a completion states the outcome and files routine checks and successful receipts in the records. These are instruction-level walkthroughs. No new live Orchestrator session or Telegram send was run; visibility in a fresh chat remains for KR Tester to observe.
- Local correction replay: start fresh Codex at the clean `f18e413db9ae6d61f8e84e4d6e91b1a682e274a8` checkout in `/private/tmp/kr-batch014-replay.HvMI5R/project`; its sole origin is the local bare fixture. Scoped diff, skills and Kanban validation passed. Replay the earlier delegated verification for PROGRESS-01/02. Require routine updates to be a stage label only; retain detail when User decision or action is needed. Do not publish or send notifications. The table below preserves observations for the delivered candidate.

| ID | Specifications | Action | Expected result | Verdict | Tested revision | Observation or evidence |
| --- | --- | --- | --- | --- | --- | --- |
| PROGRESS-01 | SPEC-022 | Start a Card and delegate it. | The current stage is visible in the original chat before the Developer returns. Each later stage appears when it starts in one line. | OK (User) | `ce9633e2614977c9c35f31294c6a3c6949aff203` | “PROGRESS-01 OK, j’ai bien vu les étapes pendant le travail.” Tested in the original chat against the isolated candidate fixture. |
| PROGRESS-02 | SPEC-022 | Delegate a Batch step running longer than a minute. | A short checkpoint or accurate ongoing status appears during the wait without being requested. | Observed in a fresh Codex chat | `ce9633e2614977c9c35f31294c6a3c6949aff203` | An unprompted checkpoint appeared during a 75.005-second delegated verification. This used a disposable Card to exercise the long delegated step. See the transcript below. |
| PROGRESS-03 | SPEC-022 | Encounter a blocker or a required User decision. | The chat gives enough context to decide or act and returns to short status after resumption. | Controlled simulation passed | `ce9633e2614977c9c35f31294c6a3c6949aff203` | The Orchestrator demonstrated a missing-file blocker, the choices and their consequences, then returned to a short progress line. See the simulation notes below. |
| PROGRESS-04 | SPEC-022 | Complete checked work and simulate a successful notification. | The chat gives a short outcome. Check details and the notification receipt remain in the records. | Controlled simulation passed | `ce9633e2614977c9c35f31294c6a3c6949aff203` | The fixture's notification smoke test passed with an injected sender. The Orchestrator demonstrated the concise completion response in the original chat. Fresh-chat behavior was not exercised. |

## Startup and actions by case

Verify visible messages in the original chat and their ordering around delegation and waits. Use disposable work and simulated notifications. Record the exact candidate and observed transcript.

### PROGRESS-01 — A Card in the original chat

The Orchestrator posted “Préparation de la carte dans le dépôt de test.”, then “Appel au KR Developer.” before delegation, and “Vérification locale du fichier.” before the Developer returned. The local test verified the four bytes `demo` and stopped without publication or Telegram. On 2026-11-15 the User gave the OK above. The parent used the designated fixture in the original chat, without starting a fresh host session.

### PROGRESS-02–04 — Tester-controlled simulations

- **PROGRESS-02.** The Tester ran a timed, no-effect subprocess in the candidate fixture from 17:05:18.980 UTC to 17:06:28.986 UTC (70.0 seconds). During the wait, the Orchestrator posted “PROGRESS-02 · Étape déléguée toujours en cours.” before the Tester reported completion. The Tester coordinated the timing. This establishes that a status line can appear before a delegated result, with no User prompt, in this chat.
- **PROGRESS-03.** The Orchestrator posted “PROGRESS-03 · Simulation d’un blocage. Le fichier attendu manque. Dans ce cas, je te demanderais de choisir entre le recréer pour reprendre ou laisser la carte en attente. La réponse est simulée pour ce test.” After the simulated decision, the Orchestrator posted “PROGRESS-03 · Simulation : vérification reprise.” This exercises the two message styles without an actual blocker or User decision.
- **PROGRESS-04.** `PYTHONDONTWRITEBYTECODE=1 python3 agents/tools/test-telegram-setup.py SetupTests.test_module_alerts_use_shared_receipts_without_colliding` passed in the candidate fixture. It checks simulated success and deduplication for module and project scopes using an injected sender. The original chat showed “PROGRESS-04 · Fin de la carte de test simulée.” without a delivery receipt. The command did not send a real notification, and the simulated completion did not publish anything.

The three simulations used the candidate fixture and the original chat. They do not carry User verdicts.

### PROGRESS-02 — Fresh Codex chat observation

The Orchestrator opened a fresh Codex chat (ID `01a1e030-a782-7bc2-8077-e53747b0aedc`) without a saved project, explicitly setting the local fixture workdir and loading its repository instructions. The fresh session verified its HEAD as `ce9633e2614977c9c35f31294c6a3c6949aff203`. The task prompt gave no progress formatting or timing instructions beyond the requirement to run the timed verification. The session received no follow-up prompt.

- The session announced Card preparation and Developer delegation before spawning the Developer.
- It posted “KR Developer a créé le fichier contenant exactement demo. La carte est en Development ; la vérification locale avec l’attente mesurée de 75 secondes vient de commencer.”
- The Orchestrator observed this further commentary while the turn was active and the delegated step had not returned (chat snapshot revision 15): “L’attente de test est toujours en cours. Le contrôle du contenu exact a réussi ; KR Developer vérifiera ensuite qu’aucun fichier n’a changé pendant l’attente.”
- The final response arrived later (revision 17). Local verification passed after a measured 75.005 seconds. The fixture commit was `ec437422`. There was no push, publication or Telegram send.

The fresh session made the long step visible without a reminder. Some status lines included more context than a brief stage label. The observation used a disposable Card and explicit workdir instruction loading, so it does not establish startup behavior for a saved project or a native Batch run. PROGRESS-03 and PROGRESS-04 remain controlled simulations.

### PROGRESS-01/02 — Local correction replay

The Orchestrator observed a fresh Codex chat (ID `01a1e037-79db-7630-b134-de2edbe17a0b`) whose starting checkout was verified in that chat as `f18e413db9ae6d61f8e84e4d6e91b1a682e274a8`. The reported commentary snapshots were:

- Revision 7: “KR Orchestrator — création de la carte dans le périmètre acceptance.”
- Revision 10: “Appel de KR Developer.”
- Revision 13: “Vérification locale — attente de test de 75 secondes.”
- Revision 21, while still active and before the final response: “Vérification locale en cours.”

The replay showed stage labels before delegation and an update during the wait. PROGRESS-03 and PROGRESS-04 were not replayed at this revision. The table above retains the observations and User verdict for the earlier candidate.
