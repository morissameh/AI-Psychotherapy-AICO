# AICO - Artificial Intelligence for psyChOtherapy

AICO is a graduation research prototype exploring conversational mental-health support
with Falcon-7B, parameter-efficient LoRA fine-tuning, and 4-bit quantization. This public
rebuild isolates the evidence-supported AI/LLM work from historical mobile, backend, and
cloud prototypes that were not verified as an end-to-end system.

The project is educational. It is not a medical product, clinical treatment, crisis
service, or replacement for a qualified mental-health professional.

## AI/LLM highlights

- Falcon-7B causal language model
- PyTorch and Hugging Face Transformers
- PEFT/LoRA with rank 32 and alpha 32
- 4-bit NF4 loading with double quantization and FP16 compute
- TRL `SFTTrainer` reconstruction
- Configuration-driven model and adapter loading
- Hugging Face text-generation pipeline
- LangChain `ConversationBufferWindowMemory` with a six-turn window
- Tests that validate configuration, prompting, safe paths, and repository hygiene without
  loading a model

## Verified architecture

```text
User text
  -> prompt formatting and bounded conversation memory
  -> Falcon-7B base model
  -> PEFT/LoRA adapter
  -> Hugging Face text-generation pipeline
  -> generated response
```

The clean code does not load models at import time. Training and inference require an
explicit function call and compatible user-supplied compute and artifacts.

## Fine-tuning configuration

| Setting | Verified value |
| --- | --- |
| Base model | `vilsonrodrigues/falcon-7b-instruct-sharded` |
| Dataset | `heliosbrahma/mental_health_chatbot_dataset` |
| Training examples | 172 |
| LoRA rank / alpha / dropout | 32 / 32 / 0.05 |
| Quantization | 4-bit NF4, double quantization, FP16 compute |
| Per-device batch size | 16 |
| Gradient accumulation | 4 |
| Optimizer | `paged_adamw_32bit` |
| Learning rate | `2e-4` |
| Maximum steps | 180 |
| Maximum gradient norm | 0.3 |
| Warmup ratio | 0.03 |
| Scheduler | Cosine |
| Maximum sequence length | 256 |

The training module asserts that the selected split still contains 172 examples. The
833-row combined experiment and 975-row candidate dataset are not represented as inputs to
the verified run.

## Dataset summary

The inspected 172-row training snapshot had one `text` field, no blanks, and no exact
duplicates. Raw datasets are not distributed. Licensing, redistribution, privacy, consent,
and generation provenance are not fully verified for all historical data.

See [the dataset card](docs/dataset-card.md) for aggregate-only documentation.

## Inference pipeline

`src/aico/inference.py` reconstructs the later documented experiment using:

- a compatible Falcon base model
- a local PEFT adapter path supplied through configuration
- 4-bit NF4 loading
- generation settings of `temperature=0.5`, `top_p=0.5`,
  `repetition_penalty=1.2`, and `max_new_tokens=512`
- six-turn LangChain conversation memory

These are recorded experiment settings, not validated optimal parameters. Optional Hugging
Face authentication is read from `HF_TOKEN`; no environment file or credential is included.

## Technology stack

| Area | Technologies |
| --- | --- |
| Model | Falcon-7B |
| Training | PyTorch, Transformers, TRL, PEFT/LoRA, bitsandbytes, Datasets |
| Inference | Transformers pipeline, PEFT, LangChain |
| Configuration and tests | Python dataclasses, JSON, standard-library `unittest` |

Flask, Firebase, a mobile UI, and a local tunnel existed as separate historical
prototypes. They are documented as boundaries rather than presented as integrated runtime
components.

## Experiment notes

The source notebook recorded a training loss of `0.020316550058002272` after 180 steps and
a runtime of `2426.9845` seconds. These are training-log values only. They do not establish
model quality, generalization, therapeutic effectiveness, or safety.

There is no verified BLEU, ROUGE, BERTScore, perplexity, clinical validation, documented
human-scored evaluation, or production deployment.

## Prototype boundaries

- No complete Flutter application is claimed.
- No mobile-to-Flask-to-Falcon integration is claimed.
- No Firebase-backed inference is claimed.
- No public or production deployment is claimed.
- No continuous-availability claim is made.
- No motivational interviewing capability or verified CBT effectiveness is claimed.

See [prototype boundaries](docs/prototype-boundaries.md) and the
[evidence-based architecture](docs/architecture.md).

## Safety and limitations

AICO is not medical diagnosis, clinical treatment, crisis support, a replacement for a
mental-health professional, or a clinically validated system. The prompt contains basic
role and crisis-language boundaries, but prompt wording is not a validated safety layer.

See [safety and limitations](docs/safety-and-limitations.md).

## Repository structure

```text
configs/             Verified training and inference settings
docs/                Architecture, dataset, experiment, provenance, and safety records
src/aico/            Clean configuration, prompting, training, and inference modules
tests/               Non-model unit and repository-security tests
assets/              Reserved for later reviewed diagrams and screenshots
pyproject.toml        Package metadata and dependencies
SECURITY.md           Credential, data, and artifact handling policy
```

Model weights, adapters, datasets, notebooks, academic reports, presentations, private
screenshots, executables, and service credentials are intentionally excluded.
