from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from aico.config import (
    InferenceConfig,
    TrainingConfig,
    load_inference_config,
    load_training_config,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class ConfigTests(unittest.TestCase):
    def test_training_config_matches_verified_experiment(self) -> None:
        config = load_training_config(REPOSITORY_ROOT / "configs/falcon-lora-training.json")

        self.assertEqual(config.verified_dataset_size, 172)
        self.assertEqual(config.lora_rank, 32)
        self.assertEqual(config.lora_alpha, 32)
        self.assertEqual(config.lora_dropout, 0.05)
        self.assertTrue(config.load_in_4bit)
        self.assertEqual(config.bnb_4bit_quant_type, "nf4")
        self.assertTrue(config.bnb_4bit_use_double_quant)
        self.assertEqual(config.bnb_4bit_compute_dtype, "float16")
        self.assertEqual(config.per_device_train_batch_size, 16)
        self.assertEqual(config.gradient_accumulation_steps, 4)
        self.assertEqual(config.optimizer, "paged_adamw_32bit")
        self.assertAlmostEqual(config.learning_rate, 2e-4)
        self.assertEqual(config.max_steps, 180)
        self.assertEqual(config.max_sequence_length, 256)

    def test_inference_config_matches_later_experiment_settings(self) -> None:
        config = load_inference_config(REPOSITORY_ROOT / "configs/inference.json")

        self.assertEqual(config.conversation_window, 6)
        self.assertEqual(config.max_new_tokens, 512)
        self.assertEqual(config.temperature, 0.5)
        self.assertEqual(config.top_p, 0.5)
        self.assertEqual(config.repetition_penalty, 1.2)

    def test_training_output_rejects_unsafe_paths(self) -> None:
        unsafe_paths = [
            "/private/adapter",
            "../adapter",
            "folder/../../adapter",
            "C:" + "\\private\\adapter",
        ]
        for unsafe_path in unsafe_paths:
            with self.subTest(path=unsafe_path), self.assertRaises(ValueError):
                replace(TrainingConfig(), output_dir=unsafe_path)

    def test_inference_adapter_rejects_unsafe_paths(self) -> None:
        unsafe_paths = [
            "/private/adapter",
            "../adapter",
            "folder/../../adapter",
            "C:" + "\\private\\adapter",
        ]
        for unsafe_path in unsafe_paths:
            with self.subTest(path=unsafe_path), self.assertRaises(ValueError):
                replace(InferenceConfig(), adapter_path=unsafe_path)

    def test_unknown_configuration_fields_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            config_file = Path(temporary_directory) / "invalid.json"
            config_file.write_text('{"unexpected": true}', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Unknown configuration fields"):
                load_inference_config(config_file)

    def test_wrong_configuration_types_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            config_file = Path(temporary_directory) / "invalid-type.json"
            config_file.write_text('{"max_new_tokens": "512"}', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "positive integer"):
                load_inference_config(config_file)


if __name__ == "__main__":
    unittest.main()
