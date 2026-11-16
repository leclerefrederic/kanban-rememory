# Guardrails

Your own rules for the agent. The agent reads this file before each Card and follows it. Where it conflicts with `orchestrator/workflow.md`, this file wins. The agent changes it only when you ask.

Edit, add or delete any line below.

## Never do

- Never force-push, and never rewrite published history.
- Never write secrets (keys, tokens, passwords) in the repository.

## Ask me first

- Before adding a dependency.
- Before deleting files or data you did not ask to delete.

## Protected files and folders

- `.env*` and any file holding credentials.

## Style and conventions

- Keep changes small and in the style of the code around them.
