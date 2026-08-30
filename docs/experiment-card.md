# Verified experiment card

## Purpose

The experiment explored parameter-efficient supervised fine-tuning of Falcon-7B for a
graduation research prototype involving conversational mental-health support.

## Recorded configuration

| Setting | Recorded value |
| --- | --- |
| Base model | `vilsonrodrigues/falcon-7b-instruct-sharded` |
| Training examples | 172 |
| Method | PEFT/LoRA with 4-bit base-model loading |
| Quantization type | NF4 |
| Double quantization | Enabled |
| Compute dtype | FP16 |
| LoRA rank | 32 |
| LoRA alpha | 32 |
| LoRA dropout | 0.05 |
| Per-device batch size | 16 |
| Gradient accumulation | 4 |
| Optimizer | `paged_adamw_32bit` |
| Learning rate | `2e-4` |
| Maximum steps | 180 |
| Maximum gradient norm | 0.3 |
| Warmup ratio | 0.03 |
| Scheduler | Cosine |
| Maximum sequence length | 256 |
| Logging interval | 10 steps |
| Save interval | 10 steps |

The LoRA target modules were `query_key_value`, `dense`, `dense_h_to_4h`, and
`dense_4h_to_h`.

## Training-log values

The original notebook recorded:

- final reported training loss: `0.020316550058002272`
- runtime: `2426.9845` seconds
- completed steps: 180

These values describe that training log only. The very low training loss is not evidence
of generalization, response quality, therapeutic value, or safety. The run did not provide
a verified evaluation dataset.

## Missing evaluation evidence

There is no verified:

- BLEU, ROUGE, or BERTScore
- perplexity
- clinical validation
- human-scored evaluation with a documented rubric
- baseline comparison
- safety benchmark
- production deployment

Any future quality claim requires a separate, versioned evaluation dataset, scoring
protocol, and reproducible results.
