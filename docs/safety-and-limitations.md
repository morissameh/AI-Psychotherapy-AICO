# Safety and limitations

AICO is an educational graduation research prototype. It is not a healthcare product.

## AICO is not

- medical diagnosis
- clinical treatment
- crisis support
- a replacement for a mental-health professional
- a clinically validated system

The prompt includes a basic boundary against diagnosis and clinical impersonation, but a
prompt is not a validated safety system. The repository does not include clinical
oversight, crisis routing, adversarial safety evaluation, monitoring, or regulatory
controls.

## Technical limitations

- The verified training run used only 172 examples.
- There is no verified held-out evaluation or quality benchmark.
- Dataset licensing, privacy, and generation provenance are incomplete.
- Generation parameters are recorded experiment settings, not validated optima.
- Model and adapter weights are not distributed.
- GPU and bitsandbytes compatibility depend on the caller's environment.
- Historical application components were not verified as an end-to-end system.

## Appropriate use

The code is suitable for portfolio review, architecture discussion, and controlled
research reproduction after the user independently verifies model and dataset terms. It
must not be used to provide real clinical or emergency services.
