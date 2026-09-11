# ECII Modern Reference v1.0.0

## Release status

**Final release verified.**

The Enterprise Computing II modernization reference implementation completed the full release gate on GitHub Actions run `34615304310` from staging commit `bd0e831b1c3d60c0e94613affa3f85b77ae148d0`.

## Verified release evidence

- Release build: 0 warnings, 0 errors
- Domain tests: 16/16 passed
- Application tests: 5/5 passed
- Architecture tests: 2/2 passed
- Integration tests: 13/13 passed
- EF Core `InitialCreate` generated and applied to a clean database
- Migration rollback to `0` and forward replay: passed
- NuGet transitive vulnerability audit: no vulnerable packages reported
- CycloneDX SBOM generated and retained
- API publish: passed
- Docker build: passed
- Development `/health` and `/health/ready`: healthy
- Production-mode `/health` and `/health/ready`: healthy
- Production Swagger exposure: disabled
- Unauthenticated production API request: HTTP 401
- Production failure injection: disabled
- High-signal committed-secret scan: passed
- Threat model, backup/restore/migration runbook, and known-limitations document: present

## Integrity

Verified source archive SHA-256:

`8bbb3ecefa26ac24cc423845e79d6283883e67a96fedcc509845d8490cc3edc2`

CycloneDX SBOM SHA-256:

`dc3e553f494044f10c04e309ac1fe21f68731791b50ff13fbba65c7822a3eff3`

Verified local Docker image ID:

`sha256:2945c4841de83991c7a304fdef7831df1eb1cb80842f1e42034837e8f0ac3b2c`

## Provenance boundary

This release is a modern clean-room/reference reconstruction and modernization of a recovered academic Enterprise Computing lineage. It does not claim sole authorship of the historical group project, real bank integration, or production deployment of the original system.

## Known limitations

The verified runtime uses SQLite. Banking gateways are simulations. OIDC production behavior is validated with representative configuration rather than a live enterprise identity-provider tenant. No regulatory payment certification, penetration-test certification, HA certification, or production financial-system claim is made.
