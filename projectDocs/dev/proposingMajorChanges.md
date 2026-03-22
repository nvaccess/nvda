# Proposing Major Changes (ADR Process)

This page explains how to propose major changes to NVDA using an Architecture Decision Record (ADR).

Use this process when an issue has the `ADR-required` label, or when your change significantly affects architecture, APIs, UX behavior, compatibility, performance, or long-term maintenance.

## What an ADR is for

An ADR is a decision document created as a GitHub issue.
It helps reviewers understand:

* what problem is being solved,
* what options were considered,
* why a technical design was chosen,
* what impact and risks are expected,
* how implementation will be delivered through PRs.

## How to create an ADR

1. Open a new issue using one of the ADR templates:

    * `ADR for major project` (form template)
    * `(Advanced) ADR for major project` (markdown template)

1. Link any relevant existing issues, PRs, discussions, or mailing list threads.
1. Fill in each section with concrete detail.
Treat this as an implementation planning document, not just an idea pitch.
1. Request feedback from NV Access and other contributors.
1. Iterate on the ADR based on feedback until there is clear agreement.
1. Do not begin large-scale implementation until the ADR is accepted/triaged for implementation.

## What is expected in an ADR

### Problem and UX expectations

* Describe the current problem and constraints clearly.
* Include user stories for UX impact, for example:
  * As a screen reader user, I want ..., so that ...
  * As an add-on developer, I want ..., so that ...
* State what user-visible behavior should change and what should remain stable.

### Options and decision rationale

* Compare realistic options, including keeping the current approach.
* Explain trade-offs and why the selected option is preferred.
* Call out known downsides and why they are acceptable.

### Impact and risk analysis

Cover expected impacts across:

* UX and accessibility behavior
* performance and reliability
* API/add-on compatibility
* security/privacy
* maintainability and developer workflow

For major risks, include mitigation and rollback/fallback plans.

### Architecture and code change planning

Provide a concrete plan that maps decisions to implementation work:

* likely modules/files and abstraction changes,
* migration strategy,
* rollout sequence,
* validation strategy (tests, manual checks, success criteria).

## Integration strategy

Every ADR should include a PR integration strategy.
In general:

* Prefer PRs around 500 LOC where possible.
* If changes are interdependent, use stacked PRs with clear ordering.
* For long-running feature work that cannot merge directly to `master`, request a `try-` branch and integrate in pieces.
* Separate unrelated work into separate issues/PRs.

When describing your plan, include:

* expected PR breakdown,
* dependency order between PRs,
* merge strategy,
* rollback strategy if integration reveals issues.

## Review and implementation flow

1. ADR is opened and discussed.
1. ADR is refined until concerns are addressed.
1. ADR is accepted/triaged for implementation.
1. Implementation PRs are opened following the ADR split/integration plan.
1. If implementation findings require changing the decision, update the ADR and re-confirm before proceeding.

## Tips for faster review

* Keep language concrete and specific.
* Use short sections and bullet points.
* Link supporting material (benchmarks, prototypes, logs, related issues/PRs).
* Clearly identify open questions and decisions needed from reviewers.
