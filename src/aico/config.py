"""Typed configuration for the documented AICO experiments."""

from __future__ import annotations

import json
from dataclasses import dataclass, fields
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Mapping, TypeVar

DEFAULT_BASE_MODEL_ID = "vilsonrodrigues/falcon-7b-instruct-sharded"
DEFAULT_DATASET_ID = "heliosbrahma/mental_health_chatbot_dataset"
VERIFIED_TRAINING_EXAMPLES = 172


def _validate_relative_path(value: str, field_name: str) -> None:
    """Reject absolute paths and parent traversal in repository configuration."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must not be empty")

    normalized = value.replace("\\", "/")
    posix_path = PurePosixPath(normalized)
    windows_path = PureWindowsPath(value)
    if posix_path.is_absolute() or windows_path.is_absolute():
        raise ValueError(f"{field_name} must be a repository-relative path")
    if ".." in posix_path.parts:
        raise ValueError(f"{field_name} must not traverse outside the repository")


def _validate_hugging_face_id(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must not be empty")
    normalized = value.replace("\\", "/")
    posix_path = PurePosixPath(normalized)
    if (
        "://" in value
        or posix_path.is_absolute()
        or PureWindowsPath(value).is_absolute()
        or ".." in posix_path.parts
    ):
        raise ValueError(f"{field_name} must be a Hugging Face repository identifier")


def _require_bool(value: object, field_name: str) -> None:
    if type(value) is not bool:
        raise ValueError(f"{field_name} must be a boolean")


def _require_positive_int(value: object, field_name: str) -> None:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")


def _require_positive_number(value: object, field_name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        raise ValueError(f"{field_name} must be a positive number")


def _require_non_empty_string(value: object, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty text")


@dataclass(frozen=True)
class TrainingConfig:
    """Configuration matching the verified 172-example training run."""

    base_model_id: str = DEFAULT_BASE_MODEL_ID
    dataset_id: str = DEFAULT_DATASET_ID
    dataset_split: str = "train"
    dataset_text_field: str = "text"
    verified_dataset_size: int = VERIFIED_TRAINING_EXAMPLES
    output_dir: str = "outputs/falcon-lora-adapter"
    load_in_4bit: bool = True
    bnb_4bit_quant_type: str = "nf4"
    bnb_4bit_use_double_quant: bool = True
    bnb_4bit_compute_dtype: str = "float16"
    lora_rank: int = 32
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: tuple[str, ...] = (
        "query_key_value",
        "dense",
        "dense_h_to_4h",
        "dense_4h_to_h",
    )
    per_device_train_batch_size: int = 16
    gradient_accumulation_steps: int = 4
    optimizer: str = "paged_adamw_32bit"
    learning_rate: float = 2e-4
    max_steps: int = 180
    max_grad_norm: float = 0.3
    warmup_ratio: float = 0.03
    lr_scheduler_type: str = "cosine"
    max_sequence_length: int = 256
    fp16: bool = True
    logging_steps: int = 10
    save_steps: int = 10
    group_by_length: bool = True

    def __post_init__(self) -> None:
        _validate_hugging_face_id(self.base_model_id, "base_model_id")
        _validate_hugging_face_id(self.dataset_id, "dataset_id")
        _validate_relative_path(self.output_dir, "output_dir")
        _require_non_empty_string(self.dataset_split, "dataset_split")
        _require_non_empty_string(self.dataset_text_field, "dataset_text_field")
        _require_non_empty_string(self.optimizer, "optimizer")
        _require_non_empty_string(self.lr_scheduler_type, "lr_scheduler_type")
        _require_bool(self.load_in_4bit, "load_in_4bit")
        _require_bool(self.bnb_4bit_use_double_quant, "bnb_4bit_use_double_quant")
        _require_bool(self.fp16, "fp16")
        _require_bool(self.group_by_length, "group_by_length")
        _require_positive_int(self.verified_dataset_size, "verified_dataset_size")
        _require_positive_int(self.lora_rank, "lora_rank")
        _require_positive_int(self.lora_alpha, "lora_alpha")
        if (
            isinstance(self.lora_dropout, bool)
            or not isinstance(self.lora_dropout, (int, float))
            or not 0 <= self.lora_dropout < 1
        ):
            raise ValueError("lora_dropout must be in the range [0, 1)")
        if not isinstance(self.target_modules, tuple) or not self.target_modules:
            raise ValueError("target_modules must not be empty")
        if not all(isinstance(module, str) and module.strip() for module in self.target_modules):
            raise ValueError("target_modules must contain non-empty strings")
        _require_positive_int(
            self.per_device_train_batch_size,
            "per_device_train_batch_size",
        )
        _require_positive_int(
            self.gradient_accumulation_steps,
            "gradient_accumulation_steps",
        )
        _require_positive_number(self.learning_rate, "learning_rate")
        _require_positive_int(self.max_steps, "max_steps")
        _require_positive_number(self.max_grad_norm, "max_grad_norm")
        _require_positive_number(self.warmup_ratio, "warmup_ratio")
        _require_positive_int(self.max_sequence_length, "max_sequence_length")
        _require_positive_int(self.logging_steps, "logging_steps")
        _require_positive_int(self.save_steps, "save_steps")
        if self.bnb_4bit_quant_type != "nf4":
            raise ValueError("the documented experiment uses NF4 quantization")
        if self.bnb_4bit_compute_dtype != "float16":
            raise ValueError("the documented experiment uses float16 compute")


@dataclass(frozen=True)
class InferenceConfig:
    """Configuration for the later documented conversational experiment."""

    base_model_id: str = DEFAULT_BASE_MODEL_ID
    adapter_path: str = "adapters/falcon-lora-adapter"
    device_map: str = "auto"
    load_in_4bit: bool = True
    bnb_4bit_quant_type: str = "nf4"
    bnb_4bit_use_double_quant: bool = True
    bnb_4bit_compute_dtype: str = "float16"
    conversation_window: int = 6
    max_new_tokens: int = 512
    temperature: float = 0.5
    top_p: float = 0.5
    repetition_penalty: float = 1.2

    def __post_init__(self) -> None:
        _validate_hugging_face_id(self.base_model_id, "base_model_id")
        _validate_relative_path(self.adapter_path, "adapter_path")
        _require_non_empty_string(self.device_map, "device_map")
        _require_bool(self.load_in_4bit, "load_in_4bit")
        _require_bool(self.bnb_4bit_use_double_quant, "bnb_4bit_use_double_quant")
        _require_positive_int(self.conversation_window, "conversation_window")
        _require_positive_int(self.max_new_tokens, "max_new_tokens")
        _require_positive_number(self.temperature, "temperature")
        if (
            isinstance(self.top_p, bool)
            or not isinstance(self.top_p, (int, float))
            or not 0 < self.top_p <= 1
        ):
            raise ValueError("top_p must be in the range (0, 1]")
        _require_positive_number(self.repetition_penalty, "repetition_penalty")
        if self.bnb_4bit_quant_type != "nf4":
            raise ValueError("the documented experiment uses NF4 quantization")
        if self.bnb_4bit_compute_dtype != "float16":
            raise ValueError("the documented experiment uses float16 compute")


ConfigT = TypeVar("ConfigT", TrainingConfig, InferenceConfig)


def _load_mapping(path: str | Path) -> Mapping[str, Any]:
    config_path = Path(path)
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to read valid JSON configuration: {config_path}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Configuration root must be a JSON object")
    return payload


def _construct_config(config_type: type[ConfigT], payload: Mapping[str, Any]) -> ConfigT:
    allowed = {field.name for field in fields(config_type)}
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise ValueError(f"Unknown configuration fields: {', '.join(unknown)}")
    try:
        return config_type(**payload)
    except TypeError as exc:
        raise ValueError(f"Invalid configuration values for {config_type.__name__}") from exc


def load_training_config(path: str | Path) -> TrainingConfig:
    payload = dict(_load_mapping(path))
    if "target_modules" in payload:
        modules = payload["target_modules"]
        if not isinstance(modules, list) or not all(isinstance(item, str) for item in modules):
            raise ValueError("target_modules must be a JSON array of strings")
        payload["target_modules"] = tuple(modules)
    return _construct_config(TrainingConfig, payload)


def load_inference_config(path: str | Path) -> InferenceConfig:
    return _construct_config(InferenceConfig, _load_mapping(path))
