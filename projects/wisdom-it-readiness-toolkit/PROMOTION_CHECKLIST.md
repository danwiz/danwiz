# Dedicated Repository Promotion Checklist

**Target repository:** `danwiz/wisdom-it-readiness-toolkit`  
**Release target:** `v0.1.0`

## Repository creation

- [ ] Create public repository with the target name.
- [ ] Set description: Practical assessments, scoring, and reports for technology readiness.
- [ ] Select MIT license.
- [ ] Add topics: `it-readiness`, `cybersecurity`, `assessment`, `small-business`, `python`, `cli`.
- [ ] Use `main` as the default branch.

## Content migration

- [ ] Move the incubator README to repository root.
- [ ] Move `src`, `tests`, `assessments`, `examples`, and `docs` to root-level directories.
- [ ] Move `SECURITY.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, and `LICENSE` to repository root.
- [ ] Copy the dedicated CI workflow to `.github/workflows/ci.yml`.
- [ ] Confirm no private data, credentials, internal-only links, or unrelated profile assets are included.

## Validation

- [ ] Run all unit tests locally or through CI.
- [ ] Run the CLI score command against synthetic responses.
- [ ] Generate the example Markdown report.
- [ ] Verify the generated report contains the expected maturity result.
- [ ] Confirm keyboard- and screen-reader-friendly documentation structure.
- [ ] Confirm security reporting instructions are correct.

## Release

- [ ] Update lifecycle status from governed working MVP to release candidate.
- [ ] Create tag `v0.1.0`.
- [ ] Publish GitHub release using `RELEASE_NOTES_v0.1.0.md`.
- [ ] Attach or link the generated example report.
- [ ] Update the profile README and Personal Brand Pages site.
- [ ] Record the repository and release in the Portfolio Master Register and DocOps register.

## Current gate decision

Documentation and accessibility review are complete for the CLI/Markdown MVP. Promotion is blocked only by creation of the dedicated repository and verification of CI on that repository.
