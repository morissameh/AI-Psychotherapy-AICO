from pathlib import Path
import re
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".json", ".md", ".py", ".toml"}
PROHIBITED_SUFFIXES = {
    ".aia",
    ".aix",
    ".bin",
    ".docx",
    ".env",
    ".exe",
    ".ipynb",
    ".pdf",
    ".ppt",
    ".pptx",
    ".pt",
    ".pth",
    ".safetensors",
}
PROHIBITED_NAMES = {
    "google-services.json",
    "GoogleService-Info.plist",
}


def repository_files() -> list[Path]:
    return [
        path
        for path in REPOSITORY_ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts
    ]


class RepositorySecurityTests(unittest.TestCase):
    def test_repository_contains_no_prohibited_artifact_types(self) -> None:
        violations = []
        for path in repository_files():
            if path.name in PROHIBITED_NAMES or path.suffix.lower() in PROHIBITED_SUFFIXES:
                violations.append(path.relative_to(REPOSITORY_ROOT).as_posix())
        self.assertEqual(violations, [])

    def test_authored_text_contains_no_secret_or_private_path_patterns(self) -> None:
        patterns = {
            "Hugging Face token": re.compile(r"hf_[A-Za-z0-9]{20,}"),
            "OpenAI-style token": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
            "private key block": re.compile("-" * 5 + r"BEGIN [A-Z ]*PRIVATE KEY"),
            "credential assignment": re.compile(
                r"(?i)(api[_-]?key|password|passwd|secret|token)\s*[:=]\s*['\"][^'\"]+['\"]"
            ),
            "private ngrok URL": re.compile(
                r"https?://[^\s'\"]*ngrok[^\s'\"]*",
                re.IGNORECASE,
            ),
            "Windows absolute path": re.compile(r"\b[A-Z]:\\", re.IGNORECASE),
            "student ID-like value": re.compile(r"\b\d{8,12}\b"),
            "merge conflict marker": re.compile(
                "|".join(("<" * 7, "=" * 7, ">" * 7))
            ),
        }

        violations = []
        for path in repository_files():
            if path.suffix.lower() not in TEXT_SUFFIXES and path.name != "README.md":
                continue
            text = path.read_text(encoding="utf-8")
            for label, pattern in patterns.items():
                if pattern.search(text):
                    relative_path = path.relative_to(REPOSITORY_ROOT).as_posix()
                    violations.append(f"{relative_path}: {label}")
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
