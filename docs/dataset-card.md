# Dataset card

## Dataset used by the verified experiment

The recorded training run used the public Hugging Face dataset
`heliosbrahma/mental_health_chatbot_dataset`.

The inspected local snapshot had:

- 172 rows
- one `text` field
- 172 distinct rows
- no exact duplicate rows
- no blank values in the required field

The clean training module asserts that the loaded split contains exactly 172 examples. If
the remote dataset changes, training stops instead of silently presenting a different run
as the verified experiment.

## Other inspected candidate data

These aggregates are documented for provenance only. Neither dataset is claimed as input
to the verified run.

| Candidate data | Rows | Structure | Exact duplicates | Verified training use |
| --- | ---: | --- | ---: | --- |
| Generated question/answer candidate | 975 | `Question`, `Answer` | 275 | No |
| Patient/psychiatrist dialogue candidate | 434 | `Patient`, `Psychiatrist` | 6 | No |

A later notebook also downloaded
`alexandreteles/mental-health-conversational-data` and constructed a combined 833-row
dataset with an 80/20 split. The trainer still received the original 172-row dataset, so
the combined data is not represented as training evidence.

## Distribution and provenance limits

- Raw datasets are not distributed in this repository.
- No dialogue examples are reproduced here.
- Dataset licensing and redistribution rights have not been fully verified.
- Privacy, consent, and generation provenance are not fully documented for every local
  candidate dataset.
- The data does not support claims of clinical coverage, motivational interviewing
  capability, or verified CBT effectiveness.

These limitations must be resolved before publishing data or using the project for a
real-world mental-health service.
