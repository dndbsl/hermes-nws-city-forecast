---
name: nws-city-forecast
description: Retrieve attributed US city weather forecasts from the official National Weather Service without an API key. Use for Los Angeles, New York, or Seattle forecasts; distinguish forecasts from current observations.
---

# NWS city forecast

Run the bundled script from this skill's directory:

```sh
python3 scripts/forecast.py --city "Los Angeles"
```

Supported cities are Los Angeles, New York, and Seattle. Python 3.10+ and outbound HTTPS access to `api.weather.gov` are required. No account or API key is needed. The script performs read-only requests and prints JSON; it does not save user data or alter a calendar.

Use `issued_at`, `timezone`, and each forecast period's start/end time when summarizing. State the units and cite `source_url`. Call the result a **forecast**, never an observed current temperature. Do not infer that a missing precipitation probability means zero. Report a provider error plainly; never invent a forecast. Forecasts can change, and this is not an emergency warning service.

For an offline functional check:

```sh
python3 scripts/forecast.py --self-test
```

The script uses fixed city coordinates, validates NWS-provided forecast endpoints, rejects redirects, limits response sizes, and times out requests. It accepts no arbitrary URLs, email addresses, or credentials.
