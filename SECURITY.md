# Security policy

## Scope

This repository contains a reconstructed educational research prototype. It does not
contain a hosted service, model weights, raw mental-health conversations, or service
credentials.

## Credential handling

- Never commit access tokens, API keys, passwords, private URLs, or service-account files.
- Optional Hugging Face authentication is read from `HF_TOKEN` at runtime.
- Do not commit `.env` files. Use a local process environment or a reviewed secret manager.
- Treat any credential found in historical project material as compromised and rotate it.

## Data and model artifacts

- Do not add raw therapy dialogues or identifiable personal data.
- Do not add model or adapter weights until licensing and redistribution rights are verified.
- Keep training outputs, caches, checkpoints, and downloaded model files outside Git.

## Reporting a security issue

Use GitHub's private security-advisory workflow for this repository. Do not open a public
issue containing a credential, private dataset record, or other sensitive evidence.
