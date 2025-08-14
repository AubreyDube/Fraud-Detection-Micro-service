Work in progress
-------------------------------
~The vision here is to build a severless platform that consumes logs and outputs a prediction pertaining to fraud.

## Fraud detector

A minimal rule-based detector is available in `fraud_detector.py`. The `evaluate_transaction`
function returns a structured decision and emits JSON logs with a correlation ID to aid
tracing.

## Run tests

```bash
pytest
```

## Security checks

Run the same security scanners locally before committing changes:

```bash
pip install pip-audit
pip-audit -r requirements.txt
```

Install [gitleaks](https://github.com/gitleaks/gitleaks#installation) and run:

```bash
gitleaks detect --source . --no-git
```
