import unittest

from aico.prompting import DEFAULT_SYSTEM_INSTRUCTION, build_prompt


class PromptingTests(unittest.TestCase):
    def test_prompt_contains_roles_and_safety_boundary(self) -> None:
        prompt = build_prompt("I had a difficult day.")

        self.assertTrue(prompt.startswith("System:"))
        self.assertIn("educational conversational research prototype", prompt)
        self.assertIn("Do not present yourself as a clinician", prompt)
        self.assertTrue(prompt.endswith("User: I had a difficult day.\nAICO:"))

    def test_prompt_keeps_only_the_configured_recent_window(self) -> None:
        history = [(f"user-{index}", f"reply-{index}") for index in range(8)]

        prompt = build_prompt("current", history, window_size=6)

        self.assertNotIn("user-0", prompt)
        self.assertNotIn("user-1", prompt)
        for index in range(2, 8):
            self.assertIn(f"User: user-{index}", prompt)
            self.assertIn(f"AICO: reply-{index}", prompt)

    def test_prompt_rejects_blank_input(self) -> None:
        with self.assertRaisesRegex(ValueError, "user_text"):
            build_prompt("   ")

    def test_prompt_rejects_malformed_history(self) -> None:
        with self.assertRaisesRegex(ValueError, "history turn"):
            build_prompt("hello", [("only one value",)])

    def test_default_instruction_does_not_claim_clinical_authority(self) -> None:
        self.assertIn(
            "replace a qualified mental-health professional",
            DEFAULT_SYSTEM_INSTRUCTION,
        )


if __name__ == "__main__":
    unittest.main()
