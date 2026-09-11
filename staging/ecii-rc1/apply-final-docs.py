from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp/ecii-work/ecii-modern-reference')


def write(rel: str, content: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + '\n')


write('docs/06-security/threat-model-v1.md', r'''
# ECII v1 Threat Model

## Scope

This threat model covers the modern .NET 8 reference implementation only. It does not describe the historical academic prototype as a production banking system and it does not claim real bank connectivity.

## Protected assets

- customer and telecom-account identifiers;
- bill, usage, payment and settlement state;
- payment idempotency keys and request fingerprints;
- accounting journals and payment-event history;
- audit records and correlation identifiers;
- OIDC subject and role claims;
- outbox and reconciliation state.

## Trust boundaries

1. Client to ASP.NET Core API.
2. API to external OIDC authority.
3. API/domain services to the relational persistence boundary.
4. Payment orchestration to simulated source/destination banking adapters.
5. Application container to host/runtime and deployment environment.
6. CI/CD runner to package registries and container base-image registries.

## Threats and controls

### Spoofing

Production mode uses OIDC/JWT and validates that Authority and Audience are configured. A fallback authorization policy requires authentication for application endpoints. Root metadata and health/readiness probes are explicitly anonymous.

### Tampering

Payment state transitions are explicit and persisted as ordered events. Optimistic concurrency detects stale writes. Financial state uses local database transactions for atomic ledger/outbox writes. Migration history is generated from the actual EF Core model and replay-tested.

### Repudiation

Operator actions are audited with principal, action, target, correlation and timing context. Payment events, settlement records and accounting journals provide additional evidence trails.

### Information disclosure

The modern model does not persist historical-style PINs or raw banking credentials. Source-account references are opaque. The idempotency request fingerprint deliberately excludes the opaque account reference. Production Swagger is disabled by default.

### Denial of service

The API applies a fixed-window rate limiter. Health and readiness endpoints are available for orchestration and recovery monitoring. The outbox has retry/dead-letter behavior instead of unbounded tight-loop retries.

### Elevation of privilege

Production API access requires an authenticated OIDC principal. Administrative operations additionally require Operator or Administrator role membership through the application authorization boundary.

### Replay and duplicate financial requests

Payment creation requires an Idempotency-Key. Idempotency is scoped by customer and normalized request fingerprint. Same-key/same-request replay returns the existing payment; same-key/different-request is rejected with HTTP 409.

### Supply-chain risk

The release gate restores from NuGet, runs a transitive vulnerability audit, generates a CycloneDX SBOM, builds from the pinned source candidate, and records source/SBOM hashes and the local Docker image ID.

## Residual risks / exclusions

- Banking adapters are simulations, not certified financial integrations.
- The verified reference runtime uses SQLite; SQL Server provider validation is not part of v1.0.0.
- OIDC startup/authorization behavior is smoke-tested with a representative synthetic issuer configuration, not a live enterprise identity provider.
- There is no external message broker; the outbox publisher is a reference implementation.
- TLS termination, WAF, managed secret storage, database encryption-at-rest and host hardening are deployment-environment responsibilities.
- No formal penetration test, performance certification, HA/failover certification or regulatory payment certification is claimed.

## Release conclusion

The controls are appropriate for an educational/reference modernization artifact. They are not sufficient evidence to market the system as a production payment platform.
''')

write('docs/08-devops/backup-restore-migration-runbook.md', r'''
# Backup, Restore and Migration Runbook

## Purpose

Provide a reproducible recovery procedure for the verified ECII reference implementation and its EF Core migration history.

## Reference database

The verified v1 reference runtime uses SQLite. Treat the database file and migration source as controlled release artifacts. Production deployments using another provider require a separate provider-specific backup and restore procedure.

## Pre-change backup

1. Stop application writes or place the service in a maintenance window.
2. Record the application version, source SHA-256 and current migration list.
3. Copy the SQLite database file to a timestamped backup location.
4. Preserve the backup separately from the deployment directory.
5. Record the backup checksum.

Example:

```bash
cp ecii-modern.db backups/ecii-modern-$(date -u +%Y%m%dT%H%M%SZ).db
sha256sum backups/ecii-modern-*.db
```

## Forward migration

```bash
export ECII_DESIGN_CONNECTION='Data Source=ecii-modern.db'
dotnet tool restore
dotnet ef migrations list \
  --project src/ECII.Infrastructure \
  --startup-project src/ECII.Api

dotnet ef database update \
  --project src/ECII.Infrastructure \
  --startup-project src/ECII.Api
```

After migration, verify `/health`, `/health/ready`, representative read operations, and the expected migration list.

## Rollback test

The final release gate proves that the generated migration can be applied, rolled back to migration `0`, and applied again on a clean verification database:

```bash
dotnet ef database update 0 \
  --project src/ECII.Infrastructure \
  --startup-project src/ECII.Api

dotnet ef database update \
  --project src/ECII.Infrastructure \
  --startup-project src/ECII.Api
```

For a live system with business data, prefer restoring a pre-change backup when a destructive or data-transforming migration cannot be safely reversed.

## Restore procedure

1. Stop the application.
2. Preserve the failed/current database for forensic comparison.
3. Restore the selected backup file to the configured database path.
4. Verify its SHA-256 against the recovery record.
5. Start the application with the matching source release.
6. Verify health/readiness.
7. Verify account, bill, payment, settlement and audit reads relevant to the recovery event.
8. Resume writes only after validation is complete.

## Recovery evidence

Capture:

- release/source SHA-256;
- database-backup SHA-256;
- pre/post migration lists;
- timestamps;
- operator performing the recovery;
- health/readiness results;
- observed discrepancies and follow-up actions.
''')

write('docs/08-devops/known-limitations-v1.md', r'''
# ECII v1 Known Limitations

## Release classification

ECII v1.0.0 is a modern reference implementation and portfolio modernization artifact. It is not a production banking, telecom billing or regulated payment service.

## Current limitations

1. **Persistence provider** — the verified runtime uses SQLite. SQL Server remains the preferred historical-lineage enterprise target, but SQL Server provider/migration validation is deferred beyond v1.0.0.
2. **Bank connectivity** — Scotia and NCB integrations are simulated gateways. No real bank APIs, settlement rails or credentials are used.
3. **Identity integration** — production OIDC configuration, authentication gating and role boundaries are exercised with representative configuration, not a live enterprise identity provider tenant.
4. **Messaging** — the transactional outbox and retry/dead-letter model are implemented, but publishing is a reference path rather than a certified external broker integration.
5. **Deployment security** — TLS termination, WAF, managed secrets, network segmentation and infrastructure hardening are deployment concerns outside this source package.
6. **Scale** — no load, soak, chaos, HA or disaster-recovery certification is claimed.
7. **Security assurance** — automated dependency audit, SBOM generation, secret-pattern scanning and threat-model review are included; no independent penetration test is claimed.
8. **Accounting scope** — application double-entry journals support reconciliation reasoning; they are not a bank general ledger, statutory accounting system or clearing ledger.
9. **Historical provenance** — the modern implementation reconstructs and modernizes a recovered academic group-project lineage. It does not imply sole authorship of the historical project or production deployment of the original system.

## Post-v1 candidates

- SQL Server provider validation and provider-specific migrations;
- real external identity-provider integration test environment;
- message-broker adapter and delivery observability;
- stronger secrets-management integration;
- load/performance baseline;
- deployment manifests and infrastructure-as-code;
- external security review.
''')

print('Added ECII v1 threat model, recovery runbook, and known-limitations documentation')
