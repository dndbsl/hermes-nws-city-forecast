# NWS city forecast for Hermes

A small, read-only Hermes skill for official US National Weather Service forecasts in Los Angeles, New York, and Seattle. Python 3.10+; no API key or account. Created for CSCI 599 Assignment 3 with Codex assistance; independently reusable and contains no course handouts, account identifiers, or credentials.

## Install in Hermes

```sh
hermes skills tap add dndbsl/hermes-nws-city-forecast
hermes skills install dndbsl/hermes-nws-city-forecast/skills/nws-city-forecast
```

Review community skill contents before confirming installation. Hermes records the resolved revision in its skill lock file. See `skills/nws-city-forecast/SKILL.md` for use and offline checks. A clean installation transcript and resolved commit hash are maintained in the private assignment evidence.

## Data and limitations

Two bounded HTTPS GET requests go to the [official NWS API](https://www.weather.gov/documentation/services-web-api). Responses are forecasts, not current observations. City choices are fixed; unsupported locations, network failures, rate limits, and NWS downtime are reported rather than replaced with fabricated data. There is no persistent cache, scheduler, account access, or write action.

MIT license covers this code. NWS data remains subject to its provider's policies.
