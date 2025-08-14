Work in progress
-------------------------------
~The vision here is to build a severless platform that consumes logs and outputs a prediction pertaining to fraud.

## Event Schema

The public `eventSchema.json` describes the format of transaction events. Sensitive fraud-detection indicators (such as velocity metrics or historical averages) have been removed. The `features` object is intentionally generic; internal feature names remain private.
