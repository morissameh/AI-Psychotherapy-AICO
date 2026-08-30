# Evidence-based architecture

## Verified AI path

```text
User text
  -> prompt formatting and bounded conversation memory
  -> Falcon-7B base model
  -> PEFT/LoRA adapter
  -> Hugging Face text-generation pipeline
  -> generated response
```

The clean implementation represents this path in four modules:

- `config.py` validates model, adapter, training, and generation settings.
- `prompting.py` builds role-labelled prompts from at most six recent turns.
- `inference.py` loads a 4-bit Falcon base model and a compatible local PEFT adapter.
- `training.py` reconstructs the verified supervised fine-tuning experiment.

No model or adapter is loaded during module import. Model loading occurs only after an
explicit call to the training or inference API.

## Artifact boundary

The repository does not distribute the Falcon base model, LoRA adapter weights, training
outputs, or raw datasets. `configs/inference.json` points to a repository-relative adapter
location that a qualified user must supply separately after confirming licensing and
compatibility.

## Historical prototypes

The graduation work also explored a mobile interface, Flask endpoints, Firebase
authentication/storage, and a local tunnel. Those components were separate prototypes.
Available evidence does not establish a complete mobile-to-API-to-Falcon execution path,
so they are intentionally excluded from the architecture above and from the clean runtime.
