# Design decisions

## 1. One suite executor

Every test run goes through the automation suite that already exists (here: Java + Cucumber, run with Maven and a tag filter). The orchestrator never grows its own test runner.

- **Why:** a second framework means two sources of truth, two sets of conventions and double the upkeep.
- **Exception:** the journey replay script. It re-checks one already-verified browser path. It is a replay tool, not a suite, and it does not accumulate tests.

## 2. One generated artifact

A generated test is exactly three things, delivered as a merge request:

1. a Cucumber `.feature` file
2. step definitions
3. page objects

Before generating, the generator reads the target repository's own contributor guide and conventions, and reuses existing steps and page objects before adding new ones.

- **Why:** reviewers already know how to review this. Nothing new to learn, nothing to special-case.

## 3. Browser findings are recorded as journeys

When an agent verifies a story in a browser, what it observed is written down as a JSON step script, built only from what the run actually saw: real selectors, real waits, real expected text.

- A journey is a **findings note**, not coverage. Regression coverage still goes to the suite through the generator.
- Journeys replay headless, so a retest takes seconds instead of a new agent session.
- Each step lists several locators. If the first goes stale, the next is tried and the report says so.

See [`journeys.md`](journeys.md).

## 4. Read-only by default

- Product code, logs and databases are read, never written.
- Anything that writes goes through one narrow, audited path behind an approval preview.
- A denied write is the guardrail working. The agent does not route around it.
- A journey that changes shared state is marked `"readOnly": false` and refuses to run without an explicit `--allow-mutation`.
- Environments flagged as not testable (production, disaster recovery) block every write and execute path outright.

## Evidence rule

Every factual claim cites its source: `file:line`, a log timestamp, or a database row. A claim with no citation is treated as unverified and is not reported as fact.
