"""Clean reconstruction of the verified AICO Falcon LoRA training experiment.

The module is inert until ``run_training`` is called. It does not contain model
weights, datasets, credentials, notebook state, or local machine paths.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .config import TrainingConfig, load_training_config


def build_quantization_config(config: TrainingConfig) -> Any:
    import torch
    from transformers import BitsAndBytesConfig

    return BitsAndBytesConfig(
        load_in_4bit=config.load_in_4bit,
        bnb_4bit_quant_type=config.bnb_4bit_quant_type,
        bnb_4bit_use_double_quant=config.bnb_4bit_use_double_quant,
        bnb_4bit_compute_dtype=torch.float16,
    )


def build_lora_config(config: TrainingConfig) -> Any:
    from peft import LoraConfig

    return LoraConfig(
        r=config.lora_rank,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=list(config.target_modules),
    )


def run_training(config_path: str | Path) -> Any:
    """Run the reconstructed experiment after explicit caller invocation.

    The dataset-size assertion prevents a changed remote dataset from being
    silently represented as the verified 172-example experiment.
    """

    from datasets import load_dataset
    from peft import prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
    from trl import SFTTrainer

    config = load_training_config(config_path)
    token = os.getenv("HF_TOKEN") or None
    auth = {"token": token} if token else {}

    train_dataset = load_dataset(
        config.dataset_id,
        split=config.dataset_split,
        **auth,
    )
    actual_size = len(train_dataset)
    if actual_size != config.verified_dataset_size:
        raise RuntimeError(
            "Dataset size differs from the verified experiment: "
            f"expected {config.verified_dataset_size}, found {actual_size}"
        )
    if config.dataset_text_field not in train_dataset.column_names:
        raise RuntimeError(
            f"Dataset is missing the required '{config.dataset_text_field}' field"
        )

    model = AutoModelForCausalLM.from_pretrained(
        config.base_model_id,
        quantization_config=build_quantization_config(config),
        device_map="auto",
        **auth,
    )
    model.config.use_cache = False
    model = prepare_model_for_kbit_training(model)

    tokenizer = AutoTokenizer.from_pretrained(config.base_model_id, **auth)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    arguments = TrainingArguments(
        output_dir=config.output_dir,
        per_device_train_batch_size=config.per_device_train_batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        optim=config.optimizer,
        learning_rate=config.learning_rate,
        max_steps=config.max_steps,
        max_grad_norm=config.max_grad_norm,
        warmup_ratio=config.warmup_ratio,
        lr_scheduler_type=config.lr_scheduler_type,
        fp16=config.fp16,
        logging_steps=config.logging_steps,
        save_steps=config.save_steps,
        group_by_length=config.group_by_length,
        push_to_hub=False,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=train_dataset,
        peft_config=build_lora_config(config),
        dataset_text_field=config.dataset_text_field,
        max_seq_length=config.max_sequence_length,
        tokenizer=tokenizer,
        args=arguments,
        packing=False,
    )
    result = trainer.train()
    trainer.save_model(config.output_dir)
    tokenizer.save_pretrained(config.output_dir)
    return result
