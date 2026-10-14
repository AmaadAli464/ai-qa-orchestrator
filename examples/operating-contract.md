# Operating contract (sample)

A short file that is always loaded into the agent's context. Everything else loads on demand, so this stays deliberately small.

## What this system is
An orchestration layer over two things it does not own:
- the product repositories, which are **read for truth**
- the automation suite, which is the **only executor** and the **only place generated tests are written**

It never becomes a test framework.

## Locked decisions
1. **One suite executor.** Every run is the suite's own command with a tag filter. The only other runner is the journey replay script, which is not a suite.
2. **One generated artifact.** A feature file, step definitions and page objects, as a merge request, written to that repository's own standards.
3. **Browser work is recorded as a journey** built only from what the run observed. If the browser tools are missing, say so and stop. Never present reasoning from source as if it were observed.
4. **Read-only by default.** Writes go through one audited path behind an approval preview. A denied write means the guardrail is working: do not route around it.

## Never hardcode a path or a name
Repositories and environments resolve through configuration. Environment names are not interchangeable across systems (a ticketing environment, a cluster namespace, a log index suffix and a database prefix can all differ for the same environment). Ask the config, never guess.

## Verdicts, not fixes
Every failure gets exactly one verdict: **product defect, test defect, environment issue, or data issue.** Never resolve a failure by loosening an assertion. Check the environment before doubting the test.

## Cite everything
`file:line`, a log timestamp, or a database row.
