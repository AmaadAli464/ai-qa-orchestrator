# Journey step scripts

A journey is a JSON file describing a browser path that was verified once and can be replayed headless.

```json
{
  "name": "login-and-browse",
  "description": "What this path proves.",
  "readOnly": true,
  "steps": [
    { "action": "goto", "url": "https://example.test/", "note": "open the site" },
    { "action": "fill",  "locators": ["[data-test='user']", "#user"], "value": "${ENV:DEMO_USER:guest}" },
    { "action": "click", "locators": ["[data-test='go']", "#go"] },
    { "action": "expect_text", "locators": [".title"], "value": "Products" }
  ]
}
```

## Fields

| Field | Meaning |
|---|---|
| `readOnly` | `true` only if replaying changes no shared state. Anything else needs `--allow-mutation`. |
| `mutates` (per step) | Marks an individual step that changes state. Also triggers the guard. |
| `locators` | Ordered fallbacks. The first one that becomes visible wins. |
| `note` | Human-readable label used in reports. |

## Actions

| Action | Needs | Does |
|---|---|---|
| `goto` | `url` | Navigates |
| `fill` | `locators`, `value` | Types into a field |
| `click` | `locators` | Clicks |
| `expect_text` | `locators`, `value` | Asserts the element's text contains the value |
| `expect_visible` | `locators` | Asserts the element appears |
| `expect_url_contains` | `value` | Asserts the current URL contains the value |

## Secrets

Never put credentials in a journey. Use `${ENV:NAME}` (required) or `${ENV:NAME:default}` (optional, e.g. a public demo login).

## Built only from observation

A step belongs in a journey only if a real run observed it: the selector resolved, the text appeared. Reasoning from source code alone does not make a step.

## Healing rules

When every locator for a step fails (exit code `2`):

- **Stale or moved element** → a healing agent may **append** a new fallback locator, found from a live accessibility snapshot. It never deletes or reorders existing ones.
- **Server error, or the element is genuinely gone** → it is reported as a failure, not healed.
- A step marked `"heal": "deny"` is never touched.

## A journey is not coverage

A journey is the note of a verification. Lasting regression coverage goes to the suite as a Cucumber feature.
