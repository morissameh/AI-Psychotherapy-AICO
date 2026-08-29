"""Configuration-driven Falcon adapter loading and conversational inference.

Nothing is loaded at module import time. Calling the loader requires the caller to
provide compatible model access, hardware, and adapter artifacts.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any

from .config import InferenceConfig, load_inference_config
from .prompting import ConversationTurn, build_prompt


def build_quantization_config(config: InferenceConfig) -> Any:
    """Create the verified 4-bit NF4 quantization configuration lazily."""

    import torch
    from transformers import BitsAndBytesConfig

    return BitsAndBytesConfig(
        load_in_4bit=config.load_in_4bit,
        bnb_4bit_quant_type=config.bnb_4bit_quant_type,
        bnb_4bit_use_double_quant=config.bnb_4bit_use_double_quant,
        bnb_4bit_compute_dtype=torch.float16,
    )


def load_text_generation_pipeline(config: InferenceConfig) -> Any:
    """Load a Falcon base model, local PEFT adapter, tokenizer, and generation pipeline."""

    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

    token = os.getenv("HF_TOKEN") or None
    auth = {"token": token} if token else {}
    base_model = AutoModelForCausalLM.from_pretrained(
        config.base_model_id,
        quantization_config=build_quantization_config(config),
        device_map=config.device_map,
        **auth,
    )
    model = PeftModel.from_pretrained(base_model, config.adapter_path)
    model.eval()

    tokenizer = AutoTokenizer.from_pretrained(config.base_model_id, **auth)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        do_sample=True,
        max_new_tokens=config.max_new_tokens,
        temperature=config.temperature,
        top_p=config.top_p,
        repetition_penalty=config.repetition_penalty,
        return_full_text=False,
    )


class AICOConversation:
    """Use LangChain window memory around the verified generation pipeline."""

    def __init__(
        self,
        config: InferenceConfig,
        generator: Callable[[str], list[dict[str, Any]]] | None = None,
    ) -> None:
        from langchain.memory import ConversationBufferWindowMemory

        self.config = config
        self.generator = generator or load_text_generation_pipeline(config)
        self.memory = ConversationBufferWindowMemory(
            k=config.conversation_window,
            memory_key="history",
            return_messages=True,
        )

    def _history_pairs(self) -> list[ConversationTurn]:
        messages = self.memory.load_memory_variables({}).get("history", [])
        history: list[ConversationTurn] = []
        pending_user: str | None = None
        for message in messages:
            message_type = getattr(message, "type", "")
            content = str(getattr(message, "content", "")).strip()
            if message_type == "human":
                pending_user = content
            elif message_type == "ai" and pending_user and content:
                history.append((pending_user, content))
                pending_user = None
        return history

    def respond(self, user_text: str) -> str:
        prompt = build_prompt(
            user_text,
            self._history_pairs(),
            window_size=self.config.conversation_window,
        )
        result = self.generator(prompt)
        if not result or not isinstance(result[0], dict):
            raise RuntimeError("The generation pipeline returned no usable response")
        response = str(result[0].get("generated_text", "")).strip()
        if not response:
            raise RuntimeError("The generation pipeline returned empty text")
        self.memory.chat_memory.add_user_message(user_text.strip())
        self.memory.chat_memory.add_ai_message(response)
        return response


def conversation_from_config(path: str) -> AICOConversation:
    """Load configuration and create a conversation; may load model artifacts."""

    return AICOConversation(load_inference_config(path))
