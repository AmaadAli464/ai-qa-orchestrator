# Cucumber example (illustrative)

This is the **shape** of what the generator agent delivers: a feature file, step definitions and a page object, written to the conventions of a Selenium + Cucumber suite.

> **Status: illustrative, not compiled in this repo.** It targets the public demo shop and follows standard Selenium 4 and Cucumber-JVM idioms, but it has no `pom.xml` here and has not been run as part of this repository. Treat it as a readable example of structure, not as a tested suite. The runnable example is [`../journey-replay`](../journey-replay).

## Conventions the generator follows
- One feature per behaviour area; scenarios named by business outcome
- Steps are reusable and phrased in business language, with no locators in the feature
- Locators and page interactions live only in page objects
- Existing steps and page objects are reused before new ones are added

## Shared steps assumed
`cart.feature` reuses login steps (`I am logged in as a standard user`, `I am on the login page`, `I log in as the locked-out user`, `I see the error ...`) that are assumed to already exist in the suite's shared step library. That is the convention in action: reuse existing steps first, and generate only the new ones (`CartSteps.java`).

## Files
- `src/test/resources/features/cart.feature`
- `src/test/java/steps/CartSteps.java`
- `src/test/java/pages/InventoryPage.java`
