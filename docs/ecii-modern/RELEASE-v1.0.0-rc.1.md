# ECII Modern Reference Architecture — v1.0.0-rc.1

## Release status

**GO — verified release candidate**

This release candidate is the modern reference implementation derived from the recovered Enterprise Computing lineage. It is a present-day modernization and must not be represented as the original 2004 or 2009 application.

## Verification evidence

Final verification was executed in GitHub Actions on .NET 8 against commit:

`94b5c5045bf4c39cb7c25f723c7b41fe5d3b6ed1`

Workflow run:

`34551787290`

Verified gates:

- Release build: 0 warnings, 0 errors
- Domain tests: 16/16 passed
- Application tests: 5/5 passed
- Architecture tests: 2/2 passed
- Integration tests: 13/13 passed
- EF Core `InitialCreate` migration generated from the actual model
- Migration applied successfully to a clean database
- Dependency vulnerability audit: no vulnerable packages reported across all nine projects
- API publish completed successfully
- Docker image build completed successfully
- Runtime gate reported: `PASS: all executable RC1 gates completed.`

## Verified source artifact

Source package:

`ecii-modern-reference-v1.0.0-rc.1-source.tar.gz`

SHA-256:

`c6421a5abc3a2c0b4e958e9c209de41bac0830b3fc4c843183d21b9c57d00837`

The GitHub Actions artifact ZIP containing the source package and checksum has artifact digest:

`1099a7e35a46fc30006ead948f9b7c218569c86de45557cde1fe170efb14e14f`

## Architecture highlights

- .NET 8 / ASP.NET Core Web API
- C# / EF Core
- layered Domain, Application, Contracts, Infrastructure, API structure
- customer-scoped idempotency with request fingerprints
- ordered payment-event history
- compensation and reconciliation workflow
- outbox processing with retry/dead-letter semantics
- accounting journal and ledger abstractions
- optimistic concurrency handling
- OIDC/JWT production authentication path
- rate limiting and security headers
- EF migrations and containerized deployment path

## Provenance boundary

The historical system and the modern implementation are intentionally separated.

Historically supported facts include participation in the earlier Enterprise Computing group project, later recovery activity, integration work, and successive archived application generations. The modern architecture, domain model, tests, resilience controls, release engineering, and security design are contemporary reconstruction work and are not claims about the original academic system.

## RC1 decision

This candidate is suitable for release-candidate preservation, demonstration, architecture review, portfolio presentation, and final hardening toward `v1.0.0`.
