# ECII Modern Reference Architecture — v1.0 Final Gate

`v1.0.0-rc.1` is verified. Promotion to `v1.0.0` should be a release-quality decision, not another architecture rewrite.

## Required before final

- Re-run the complete RC verification gate from the exact final commit.
- Confirm all automated tests remain green.
- Confirm EF migration history is stable and reproducible.
- Confirm dependency vulnerability audit remains clean.
- Confirm Docker build remains reproducible.
- Confirm production Swagger remains disabled by default.
- Confirm failure injection is disabled in production configuration.
- Confirm OIDC authority/audience validation path is documented and tested with a representative provider configuration.
- Confirm no secrets, credentials, PINs, tokens, or environment-specific connection strings are committed.
- Confirm release artifact checksum and source provenance are recorded.

## Strongly recommended hardening

These items may be completed before `v1.0.0` or explicitly deferred with an ADR/issue if they are outside the reference implementation's intended scope:

- signed container image and provenance attestation;
- SBOM attached to the final release;
- CodeQL/SAST and secret-scanning gate;
- deployment smoke test against the selected production database provider;
- health/readiness verification in a running container;
- correlation-ID propagation and metrics verification;
- backup/restore and migration rollback runbook validation;
- operator/admin authorization test against real OIDC claims;
- final threat-model review.

## Freeze criteria

Do not add new product features between RC1 and final unless they address a release-blocking defect. Changes should be limited to:

- bug fixes;
- security fixes;
- release documentation;
- deployment/readiness corrections;
- provenance and portfolio documentation.

## Final release evidence pack

The `v1.0.0` evidence pack should contain:

1. exact commit SHA;
2. test summary;
3. migration identifier and generated SQL;
4. vulnerability audit output;
5. SBOM;
6. Docker image digest;
7. source archive SHA-256;
8. release notes;
9. known limitations;
10. provenance statement.

## Release decision

Current state: **RC verified / final release pending hardening review**.
