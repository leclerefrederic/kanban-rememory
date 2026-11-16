"""Phase performance line: durations from the Card History, token totals from host session logs."""

from datetime import datetime
import json
import os
from pathlib import Path
import re

from .markdown import moves

CLAUDE_FIELDS = (("input", "input_tokens"), ("cache write", "cache_creation_input_tokens"),
                 ("cache read", "cache_read_input_tokens"), ("output", "output_tokens"))
CODEX_FIELDS = (("input", "input_tokens"), ("cached input", "cached_input_tokens"), ("output", "output_tokens"))


def minutes(start, end):
    total = round((end - start).total_seconds() / 60)
    return "<1 min" if total < 1 else f"{total} min" if total < 60 else f"{total // 60} h {total % 60:02d} min"


def card_duration(card_text, active, completed):
    """From the first move into an active stage to the move into the completed stage."""
    recorded = moves(card_text)
    began = next((at for at, stage in recorded if stage in active), None)
    done = next((at for at, stage in recorded if stage == completed), None)
    return minutes(began, done) if began and done else None


def lines(path):
    try:
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                try:
                    yield json.loads(line)
                except ValueError:
                    continue
    except OSError:
        return


def moment(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def claude_tokens(roots, start, end):
    """Per-message usage in the Claude Code transcripts of these working directories."""
    home = Path(os.environ.get("KR_CLAUDE_HOME", Path.home() / ".claude")) / "projects"
    seen = {}
    for root in roots:
        for log in (home / re.sub(r"[^A-Za-z0-9]", "-", str(root))).glob("*.jsonl"):
            for entry in lines(log):
                message, when = entry.get("message"), moment(entry.get("timestamp"))
                if isinstance(message, dict) and isinstance(message.get("usage"), dict) and when and start <= when <= end:
                    seen[message.get("id") or (log.name, entry.get("uuid"))] = message["usage"]
    if not seen:
        return None
    return {key: sum(usage.get(key, 0) for usage in seen.values()) for _, key in CLAUDE_FIELDS}


def codex_tokens(roots, start, end):
    """Growth of the cumulative token counters of Codex rollouts started in these directories."""
    home = Path(os.environ.get("KR_CODEX_HOME", Path.home() / ".codex")) / "sessions"
    wanted = {str(root) for root in roots}
    total = {key: 0 for _, key in CODEX_FIELDS}
    found = False
    for log in home.glob("*/*/*/rollout-*.jsonl"):
        before = inside = cwd = None
        for entry in lines(log):
            payload = entry.get("payload") or {}
            if entry.get("type") == "session_meta":
                cwd = payload.get("cwd")
            usage = (payload.get("info") or {}).get("total_token_usage") if payload.get("type") == "token_count" else None
            when = moment(entry.get("timestamp"))
            if usage and when:
                if when < start:
                    before = usage
                elif when <= end:
                    inside = usage
        if cwd in wanted and inside:
            found = True
            for key in total:
                total[key] += inside.get(key, 0) - (before or {}).get(key, 0)
    return total if found else None


def tokens_text(name, usage, fields):
    if not usage:
        return f"Tokens ({name}): unavailable."
    return f"Tokens ({name}): " + ", ".join(f"{label} {usage[key]:,}".replace(",", " ") for label, key in fields) + "."


def report(started, end, card_texts, active, completed, roots):
    """One journal paragraph: phase and Card durations, then the token totals."""
    durations = "; ".join(f"{card} {card_duration(text, active, completed) or 'n/a'}" for card, text in card_texts)
    return (f"Duration: {minutes(started, end)} ({durations}). "
            f"{tokens_text('Claude Code', claude_tokens(roots, started, end), CLAUDE_FIELDS)} "
            f"{tokens_text('Codex', codex_tokens(roots, started, end), CODEX_FIELDS)}")
