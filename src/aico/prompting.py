"""Prompt construction for the AICO research prototype."""

from __future__ import annotations

from collections.abc import Sequence

ConversationTurn = tuple[str, str]

DEFAULT_SYSTEM_INSTRUCTION = (
    "You are AICO, an educational conversational research prototype. "
    "Respond with calm, respectful, general emotional-support language. "
    "Do not present yourself as a clinician, diagnose conditions, prescribe treatment, "
    "or claim that you replace a qualified mental-health professional. "
    "If a message suggests immediate danger or a crisis, encourage the person to contact "
    "local emergency services or a trusted qualified professional."
)


def _clean_message(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty text")
    return value.strip()


def build_prompt(
    user_text: str,
    history: Sequence[ConversationTurn] = (),
    *,
    window_size: int = 6,
    system_instruction: str = DEFAULT_SYSTEM_INSTRUCTION,
) -> str:
    """Build a bounded, role-labelled prompt from recent conversation turns."""

    if window_size <= 0:
        raise ValueError("window_size must be positive")

    cleaned_user_text = _clean_message(user_text, "user_text")
    cleaned_instruction = _clean_message(system_instruction, "system_instruction")
    recent_history = history[-window_size:]

    lines = [f"System: {cleaned_instruction}", "Conversation:"]
    for index, turn in enumerate(recent_history):
        if not isinstance(turn, tuple) or len(turn) != 2:
            raise ValueError(f"history turn {index} must be a (user, assistant) tuple")
        human_text = _clean_message(turn[0], f"history[{index}].user")
        assistant_text = _clean_message(turn[1], f"history[{index}].assistant")
        lines.extend((f"User: {human_text}", f"AICO: {assistant_text}"))

    lines.extend((f"User: {cleaned_user_text}", "AICO:"))
    return "\n".join(lines)
