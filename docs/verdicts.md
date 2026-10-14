# Verdicts

Every failure ends with exactly **one** verdict. The point is to decide *what is wrong* before deciding what to change.

| Verdict | Meaning | Typical evidence | Next step |
|---|---|---|---|
| **Product defect** | The application behaves incorrectly | Reproducible in the browser; log error; database state contradicts the response; code path missing a check | File a bug with evidence |
| **Test defect** | The check is wrong or stale | Locator changed legitimately; the expectation contradicts the requirement | Fix the test, with review |
| **Environment issue** | The environment, not the product, is at fault | Service down, wrong build deployed, config drift, expired certificate | Fix or wait for the environment, then re-run |
| **Data issue** | The test data is missing, stale or consumed | Record absent, balance spent, state already changed | Reset or prepare data, then re-run |

## Rules

1. **Never resolve a failure by loosening an assertion.** Weakening a check hides the verdict instead of reaching it.
2. **Check the environment before doubting the test.** Most failures that look like test problems turn out to be environment drift.
3. **One verdict only.** If two seem to apply, the investigation is not finished.
4. **Cite it.** A log timestamp, a database row, or a `file:line`.

## Replay exit codes map to verdicts

| Runner exit | Likely verdict to investigate first |
|---|---|
| `1` assertion failed | Product defect |
| `2` every locator exhausted | Test defect (stale locator), unless the element is genuinely gone, which is a product defect |
| `3` blocked | Not a failure: the guard worked |

## Example verdict card

```
VERDICT   Product defect
LOG       10:42:11  ERROR  CartService  NullPointerException at addItem()
DB        carts.item_count = 0 while the request returned HTTP 200
CODE      CartController.java:87  null check missing before addItem()
BLAST     Same pattern found in 2 other endpoints
```

*(Illustrative data.)*
