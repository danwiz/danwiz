# ECII Runtime Verification Correction — v0.9.1-rc.3

## Status

`v0.9.1-rc.3` is a **runtime-fix candidate**, not yet a runtime-verified release candidate.

## Corrected verification record

The complete `v0.9.0-rc.2` archive was recovered from the original generated ZIP and inspected directly. The later `...runtime-verification-gate-updated.zip` artifact contained only `README.md` and `CHANGELOG.md`, so it is not treated as a complete project package.

The current execution container was checked again and does not provide `dotnet`, `csc`/`mcs`, `msbuild`, or Docker, and shell outbound networking is unavailable. Therefore no claim is made that NuGet restore, C# compilation, xUnit execution, EF migration execution, or Docker build succeeded in this environment.

## Corrective changes applied locally

- Scoped idempotency to `(CustomerId, IdempotencyKey)` in lookup and persistence uniqueness.
- Replaced SQL Server-style `RowVersion` assumptions with a provider-neutral GUID concurrency token refreshed by `AppDbContext.SaveChangesAsync`.
- Fixed the outbox pending query to filter persisted `DeadLetteredAt` rather than the computed `IsDeadLettered` property.
- Added isolated per-factory SQLite databases for integration tests.
- Added Development-only `EnsureCreatedAsync` fallback while non-Development relational startup remains migration-only.
- Standardized persisted monetary values to `decimal(19,4)`.
- Changed payment-event deletion behavior from cascade to restrict.
- Removed the redundant explicit `Microsoft.AspNetCore.Diagnostics.HealthChecks` package reference.

## Static checks completed

- C# brace parity passed.
- No stale `RowVersion` symbol remains.
- No stale unscoped `GetByIdempotencyKeyAsync(string...)` signature remains.
- No EF query still filters through `!x.IsDeadLettered`.
- Solution project paths remain present.

## Promotion gate

Promotion to `v1.0.0-rc.1` remains blocked until a real .NET 8 runner completes restore, Release build, full tests, EF migration generation/application, concurrency and transaction verification, Docker build, vulnerability audit, SBOM generation, and OIDC production-configuration validation.
