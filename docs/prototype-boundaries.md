# Prototype boundaries

## Verified core

The public rebuild contains only the evidence-supported AI core:

- Falcon-7B configuration
- PEFT/LoRA fine-tuning reconstruction
- 4-bit NF4 model-loading configuration
- Hugging Face text-generation pipeline construction
- bounded LangChain conversation memory
- prompt construction and non-model tests

## Historical separate prototypes

The graduation archive contains evidence of separate experiments involving:

- mobile UI screens
- Flask routes
- Firebase authentication and storage
- a local tunnel used during development

These artifacts do not prove an integrated or deployable application. They are not
included in the clean repository because the available implementations were incomplete,
contained unsafe development assumptions, or included private configuration.

## Claims intentionally excluded

This repository does not claim:

- a complete Flutter application
- a verified mobile-to-Flask-to-Falcon workflow
- Firebase-backed model inference
- a deployed API
- continuous availability
- production readiness

The distinction protects the portfolio from presenting historical design intent as
implemented behavior.
