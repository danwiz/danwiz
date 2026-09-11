# Case Study — Recovered Legacy Distributed .NET Billing & Payment System

## Executive summary

This case study documents the recovery, analysis, modernization, and verification of a legacy academic distributed billing and payment system associated with the Enterprise Computing course lineage.

The work spans four distinct evidence layers:

1. a recovered early ASP.NET/VB.NET implementation with ASMX services and SQL Server databases;
2. a formal 2009 Enterprise Computing II assignment specification for a distributed telecom billing/payment system;
3. a later C# redevelopment archived in 2011 with LIME, NCB, Scotia, reusable controls, web services, MDF/LDF databases, and SQL scripts;
4. a contemporary .NET 8 reference implementation built to preserve the business scenario while replacing obsolete architecture and unsafe design assumptions.

## Historical system

The recovered historical implementation used:

- ASP.NET Web Forms
- VB.NET in the earlier generation
- C# in the later redevelopment
- ASMX/SOAP web services
- SQL Server databases
- stored procedures and views
- session state and cookies
- institution-specific service layers for telecom and banking functions

The original payment flow coordinated separate operations across the telecom, Scotia, and NCB databases. No evidence of a distributed transaction coordinator was found. That makes cross-database atomicity and duplicate-payment handling material modernization concerns.

## Modernization objectives

The modern reference implementation preserves the core business invariant:

`authenticated telecom customer -> account/billing -> bank debit/credit simulation -> payment -> telecom balance update -> review/audit`

while replacing the historical implementation model with:

- explicit domain and application boundaries;
- modern identity separation;
- resilient payment orchestration;
- idempotency and request fingerprints;
- optimistic concurrency;
- ordered payment-event history;
- compensation and reconciliation states;
- outbox processing;
- accounting/ledger records;
- structured API contracts and Problem Details;
- production OIDC authentication path with authenticated fallback authorization;
- automated tests, migrations, SBOM generation, containerization, and CI verification.

## Architecture

The reference solution is organized into:

- `ECII.Domain`
- `ECII.Application`
- `ECII.Contracts`
- `ECII.Infrastructure`
- `ECII.Api`
- automated test projects for domain, application, architecture, and integration behavior

Principal bounded areas include Customer, Telecom Account, Billing, Usage, Payments, Banking Integration, Reconciliation, Notifications, and Audit.

## Payment reliability model

The historical sequence of Scotia withdrawal -> NCB deposit -> telecom balance update is modeled as a process rather than a single distributed transaction.

The modern design adds:

- idempotent payment creation;
- request fingerprint conflict detection;
- persisted payment states;
- ordered transition events;
- source and destination compensation paths;
- reconciliation-required states;
- ledger and journal records;
- outbox retry/dead-letter processing;
- auditability for privileged actions.

## Final runtime verification

The `v1.0.0` source passed the complete GitHub-hosted .NET 8 release and hardening gate with:

- 0 compiler warnings
- 0 compiler errors
- 16/16 domain tests passing
- 5/5 application tests passing
- 2/2 architecture tests passing
- 13/13 integration tests passing
- real EF Core `InitialCreate` generation and clean-database application
- migration rollback to `0` and forward replay
- no vulnerable packages reported by the NuGet vulnerability audit
- CycloneDX SBOM generation
- successful API publish
- successful Docker build
- healthy development and production-mode health/readiness probes
- production Swagger disabled
- unauthenticated production API access returning HTTP 401
- production failure injection disabled
- representative OIDC Authority/Audience startup validation
- high-signal committed-secret scan passing
- final threat model, recovery runbook, and known-limitations documentation included

GitHub Actions run: `34615304310`

Final source SHA-256:

`8bbb3ecefa26ac24cc423845e79d6283883e67a96fedcc509845d8490cc3edc2`

CycloneDX SBOM SHA-256:

`dc3e553f494044f10c04e309ac1fe21f68731791b50ff13fbba65c7822a3eff3`

## Portfolio-safe attribution

Supported historical attribution is intentionally conservative:

- participated in the earlier Enterprise Computing group project;
- retained and circulated project materials;
- initiated or participated in legacy recovery work;
- sought database restoration;
- participated in integration and hosted-build remediation;
- later reconstructed and modernized the system using recovered evidence.

This case study does **not** claim sole authorship of the original academic project, production banking integration, commercial telecom deployment, or an unverified final course grade.

## Engineering value demonstrated

The project demonstrates:

- legacy code archaeology;
- evidence-based requirements reconstruction;
- architecture modernization;
- distributed workflow design;
- financial-transaction resilience concepts;
- API and domain modeling;
- EF Core persistence and migrations;
- automated testing and regression repair;
- CI/CD and containerization;
- security remediation;
- release engineering, SBOM generation, and provenance discipline.

## Known limitations

The verified runtime uses SQLite, while SQL Server remains a future provider-validation target. Banking gateways are simulations. The OIDC production path is validated with representative configuration rather than a live enterprise identity-provider tenant. No production payment certification, penetration-test certification, HA certification, or regulatory financial-system claim is made.
