Work in progress
-------------------------------
~The vision here is to build a severless platform that consumes logs and outputs a prediction pertaining to fraud.

## Fraud detector

A minimal rule-based detector is available in the `fraud_detector` package. The
`evaluate_transaction` function returns a structured decision and emits JSON
logs with a correlation ID to aid tracing.

Rules are registered in a central registry so each can be tested in isolation.
Additional rule modules can be loaded by setting the `FRAUD_RULE_MODULES`
environment variable to a comma-separated list of module paths. Each module
should register rules using the provided decorator.

### Logging

The module uses a logger named `fraud_detector` that outputs one JSON record per
line. Call `fraud_detector.configure_logging()` to attach the default
`StreamHandler`, or pass in a custom logger so applications can manage logging
themselves. The handler is only added if none are present to avoid duplicate
logs.

## Run tests

```bash
python -m pytest
```

## Security checks

Run the same security scanners locally:

```bash
pip install pip-audit
pip-audit -r requirements.txt
```

Install [gitleaks](https://github.com/gitleaks/gitleaks#installation) and run:

```bash
gitleaks detect --source . --no-git
```
