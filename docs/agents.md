# Agents

Five narrow agents instead of one general one. Each has a clear input, a clear output and a boundary it cannot cross.

| Agent | Input | Output | Cannot |
|---|---|---|---|
| **Researcher** | Story key, environment, resolved repo coordinates | A cited research brief (story, comments, existing test cases, merge requests, implementing code) | Write to the ticketing system, repository or any database |
| **Scout** | A live screen with no page object yet | Findings file: selectors that resolved, step order, real waits, network calls seen | Produce a test, or accumulate a suite of its own |
| **Generator** | A gap description, target area, the suite's conventions | Feature, step definitions and page objects in the working tree | Commit, push or open the merge request |
| **Healer** | A `LOCATOR-EXHAUSTED` step plus a live accessibility snapshot | An append-only fallback locator and a log line | Heal a server error, a `heal: deny` step, or onto a forbidden control |
| **Investigator** | A bug ticket, resolved coordinates, an environment | A cited root cause, a blast-radius sweep and a proposed fix as a diff | Mutate any system or apply the fix |

## How they fit

```
story ─► Researcher ─► test cases ─► (Scout) ─► browser verification ─► journey
                                                        │
                                              failures ─┤
                                                        ├─► Investigator ─► verdict + proposed fix
                                           stale locator┴─► Healer
verified cycle ─► Generator ─► feature + steps + page objects ─► merge request ─► human review
```

## Why narrow roles

- Each agent can be given **only the tools it needs**. The investigator has no write tools at all.
- Failures are easy to attribute: a bad brief is the researcher's, a bad locator is the scout's.
- Boundaries are easier to audit than one agent trusted to behave.

See [`../examples/agents/`](../examples/agents/) for sample definitions.
