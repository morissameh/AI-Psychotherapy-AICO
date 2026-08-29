# Source provenance

## Reconstruction method

This repository was rewritten from scratch using an offline graduation-project archive as
read-only evidence. Raw notebooks and scripts were not copied because they contained
notebook state, local-machine assumptions, private configuration, or credential risks.

Paths below are relative to that private archive; the archive itself is not distributed.

## Training references

- `Codes/finetune_falcon_7b_sharded_freeGPU(Good).ipynb`
- `Codes/Falcon_test(last_fintuned).ipynb`
- `Codes/Falcon_test(last_fintuned and good code).ipynb`

The first notebook is the source for the verified 172-example run. The later notebooks are
used only to document experimental differences and the unused combined-data split.

## Inference references

- `Codes/final_model_V2.py`
- `Codes/final_model_V3.py`
- `Codes/app.py.txt`

Only the verified concepts were retained: Falcon loading, 4-bit NF4 configuration, PEFT
adapter loading, text generation, prompt formatting, and bounded conversation memory.

## Dataset references

- `dataset/refrences.txt`
- `Codes/datasets/New Text Document.txt`
- `dataset/data_111.csv` - aggregate inspection only
- `dataset/best dataset with medicine question/moris_data_975_row.csv` - aggregate inspection only
- `psychiatrist_patient_dialogues.csv` - aggregate inspection only

No raw dialogue was transferred into this repository.

## Model metadata references

- `model/model_fine-tuned-by moris(24-6-2024)/adapter_config.json`
- `model/trained_model_recently/adapter_config.json`

The clean configuration follows the verified notebook run and records later inference
settings separately. No adapter weights or model archives are included.

## Sanitization guarantees

- No source credential value was copied.
- No private URL or local absolute path was copied.
- No raw notebook, dataset, model artifact, report, or presentation was copied.
- Authentication, when required, is read only from the caller's `HF_TOKEN` environment
  variable.
