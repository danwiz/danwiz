# Car Dealership — PBKDF2 security parity and legacy credential migration

**Date:** 2026-10-29 ET  
**Status:** PROPOSED SECURITY DESIGN — **NO-GO for release or account migration**.  
**Workstream:** [integration #85](https://github.com/danwiz/project0-cardealership/issues/85), [authorization #29](https://github.com/danwiz/project0-cardealership/issues/29), [portfolio audit](https://github.com/danwiz/danwiz/pull/25).  
**Scope:** `danwiz/project0-cardealership` `master` vs CI-verified draft #104.

## 1. Source-verified security regression

| Property | Source in `master` | Source in long #104 leaf | Integration requirement |
| --- | --- | --- | --- |
| Algorithm | PBKDF2WithHmacSHA256 | Same | Preserve algorithm or approve separately assessed migration |
| Default new hash work factor | 600,000 iterations | 120,000 iterations | **No reduction in new-hash strength**; benchmark and document approved floor |
| Accepted encoded iteration limits | 600,000 to 2,000,000 | No explicit cap; takes integer from stored string | Reject excessive work before invoking PBKDF2; old records require a separate bounded and authenticated migration route |
| Encoded size | Max 512 characters | No explicit size cap | Cap input bytes before split/Base64 decode |
| Salt | Exactly 16 bytes | Not verified before derivation | Validate before derivation |
| Output key | Exactly 256 bits | Length taken from encoded `expected` field | Validate fixed length, constant-time compare |
| Regression | `rejectsUntrustedWorkFactorsBeforeHashing` present | Missing | Retain master test + additional hostile lengths and cases |

OWASP Password Storage Cheat Sheet identifies PBKDF2-HMAC-SHA256 with **600,000 iterations** as the recommended work factor when PBKDF2 is required for FIPS environments: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html . A fast hash/low work factor makes offline guessing cheaper; an unbounded encoded work factor can cause resource exhaustion on authentication attempts.

## 2. Safe proposed migration state machine

```text
credential submitted
  → bounded input/username checks
  → load *authorized persisted* account row (not client-supplied hash)
  → inspect credential scheme/version + encoded size, format, salt/key lengths
  → reject malformed / untrusted iteration counts before doing PBKDF2
  → approved modern hash → constant-time verification → normal session issuance
  → approved legacy hash (120,000 only if recognized in persisted legacy cohort)
       → bounded verification against existing persisted hash
       → on successful authentication: generate new random-salted ≥600k hash
       → conditional compare-and-swap update of encoded credential in same DB
       → atomically rotate persistent session_revision via owner trigger
       → audit work-factor migration without logging plaintext or hashed secret
       → authenticate only to the newly current account/session generation
  → failed verification / race / read-only policy → fail closed or require separate reauthentication
```

**Important:** Merely allowing 120k encoded strings in a public generic `matches()` method can create a downgrade pathway; legacy acceptance must be tied to *trusted persisted account state*, a bounded, explicitly time-limited migration policy and a clear audit record. If an existing user cannot authenticate, do not automatically weaken global verification; use an approved account recovery or credential reset. Apply rate limiting before expensive KDF computation.

## 3. Implementation and test plan

1. **Parity prototype:** An isolated branch `security/integration-candidate-master-pbkdf2-parity-20261029` created from long #104 immutable commit `45eccdc73ce36d4298326498a3603e2363251fd6`. Exact `master` PBKDF2 source and tests copied into prototype at `2ebcebb62b7668f5e9c89393726e183c4eb8abe2`. This only tests **strict master semantics**, not legacy credential migration or the short branch.
2. **Inventory legacy hashes:** In an authorized disposable read-only fixture, count encoded iteration/version cohorts, invalid encodings and unique account states; do not export hashes into PR comments or public audit logs. No real account data scanned in this task.
3. **Specify policy:** Permit current ≥600k secure hashes and, only during migration, exact legacy 120k encodings with bounded parser and fixed salt/key lengths. Set account-level migration state and expiry. Do not accept unlimited iteration counts; preserve master max verification cost for new hashes.
4. **Atomic upgrade:** On successful legacy verification, generate strong new salt + hash, use `updateCredentialIfCurrent(username, oldHash, newHash)` or an equivalent CAS, and check that the DB owner rotates `session_revision`. On CAS failure, reread and reauthenticate; never issue a session using a stale revision.
5. **Audit and telemetry:** Log account pseudonymous ID, scheme version, migration outcome, error category and rate-limit outcome, but never plaintext, encoded hash, salts, bearer tokens or raw DB credentials. Use approved log retention/privacy settings.
6. **Regression:** Tests for 120k legacy success→600k rehash; 600k success; malformed/high work factor rejected before derivation; 0, negative and huge iteration counts; oversized encoded input; truncated/malformed salt/key; duplicate race; stale session revocation on rehash; new registration always strong; no lockout on authorized migration.
7. **Performance:** Benchmark typical and p95 verification latency under configured CI/staging concurrency; ensure authentication rate limits and workload isolation. A 5× higher iteration count may materially increase CI/auth CPU use; do not lower protection merely to keep a test fast.
8. **Release sequencing:** Preserve original schemas and backups; rehearse rollback without reactivating older sessions or losing rehashed credentials. Deploy only after DBA/security review, independent signoff and final exact candidate SHA with Java 11/17, PostgreSQL 16, #85 integration and complete audit evidence.

## 4. Verification and acceptance register

| Gate | Evidence now | Disposition |
| --- | --- | --- |
| Source regression confirmed | Direct blob comparison of master and #104 PBKDF2 source/test; 600k vs 120k and missing bound checks | **CONFIRMED risk** |
| Strict master file/test copied | Isolated prototype head `2ebcebb62b7668f5e9c89393726e183c4eb8abe2`; identical file blobs as `master` | **Done, only on isolated branch** |
| Java 11/17 CI on parity prototype | GitHub run [#40986769490](https://github.com/danwiz/project0-cardealership/actions/runs/40986769490) **pending when this document was authored** | **Not yet verified** |
| Legacy stored-hash cohort inventory | No real private credential data inspected | **Not performed** |
| Legacy hash migration and atomic CAS | Design only | **Not implemented** |
| Short-branch and nine master-path parity | 16-overlap/9-short/9-master register exists | **Unmerged** |
| Independent approval / production release | No signoff | **NO-GO** |

This is a review and test-design artifact. It does not authorize a public credential corpus scan, credential export, production security downgrade, main/master merge or release.


## 5. Opt-in migration implementation checkpoint — 2026-10-29 ET

On the **isolated integration-candidate branch only** (`security/integration-candidate-master-pbkdf2-parity-20261029`), a **disabled-by-default** legacy credential upgrade was implemented and a new regression suite added. This does not alter `master`, #104 or the separate Maven portfolio repository.

- `src/com/revature/service/LegacyPbkdf2CredentialUpgrade.java`: recognizes **only** exact `pbkdf2$120000$<16-byte salt base64>$<32-byte key base64>` from a trusted persisted account, with **512-character maximum input**, exact canonical Base64 encoding, no variable KDF iteration count or output size, fixed 120k and constant-time comparison. Must be explicitly constructed with a trusted credential writer; the normal login service has **no migrator configured**.
- `UserLoginService.authenticate`: tries the existing strict `Pbkdf2PasswordHasher` first. Only an explicitly injected migrator may verify a historical account. Upon successful legacy verification it generates a current strict 600k hash, uses `updateCredentialIfCurrent` CAS, reloads the stored account and checks its new hash/role and rotated `sessionRevision` **before** returning an authenticated account. A stale CAS, wrong password, invalid encoding or missing migrator yields no login, not a downgrade.
- `LegacyPbkdf2CredentialUpgradeTest`: exact historical hash rejected by default; opt-in in-memory and JDBC/H2 successful migration; wrong-password denial without writes; malformed/giant/out-of-range work factors rejected; CAS conflict denied. The tests use synthetic CI-only credentials, not real customer data.
- The previously verified strict-master parity at SHA `2ebcebb62b7668f5e9c89393726e183c4eb8abe2` passed **331 tests each on Java 11 and 17** in [CI #40986769490](https://github.com/danwiz/project0-cardealership/actions/runs/40986769490), zero fail/error/skip, including `Pbkdf2PasswordHasherTest` four non-skipped tests.
- The migration implementation's exact head `eadc05748a1c0481d16bf97f3edeebc086170d94` has CI [#40987971029](https://github.com/danwiz/project0-cardealership/actions/runs/40987971029) **COMPLETED SUCCESS**: Java 11 and Java 17 each **337 tests with 0 failures, 0 errors, 0 skips**; both job logs explicitly show **6 non-skipped `LegacyPbkdf2CredentialUpgradeTest` cases** and 4 strict PBKDF2 tests, plus the 2 PostgreSQL COMMIT transport tests. Both test and package verification report `BUILD SUCCESS`.

### Explicitly still missing

1. An approved operator-only / credential-only SQL role and secure migration *installation*. The normal runtime does **not** auto-migrate stored legacy accounts.
2. A trusted inventory of actual persisted 120k account cohorts. Public GitHub CI synthetic records are **not** evidence of real data.
3. End-to-end authenticated runtime session issuance after upgrade, role/rate-limit/audit integration, and independent reviewer signoff.
4. Migration window expiry, special handling for restored database backups and account rollback, and production-safe failure management. No production queries or write actions were executed.

**Release stays NO-GO until exact-SHA CI, authenticated runtime integration and migration/rollback controls pass independent review.**


## 6. Exact-head CI verified migration candidate — 2026-10-29 ET

[GitHub Actions #40987971029](https://github.com/danwiz/project0-cardealership/actions/runs/40987971029) completed **SUCCESS** for exact head `eadc05748a1c0481d16bf97f3edeebc086170d94`. **337 tests per Java version (11 and 17), zero failures/errors/skips**, with Maven package lifecycle successful. The six synthetic migration tests executed in both Java environments; strict work-factor test, PostgreSQL16 session-revision and purchase COMMIT-fault tests remained part of the passing matrix.

**Tested but still not installed:** explicit legacy credential writer capability is opt-in. Normal application composition still denies 120k hashes. The successful migration tests use **synthetic in-memory and H2/JDBC fixture accounts** only; no real account cohort, existing production database or customer password was accessed. An external operator with approved privileges and staged deployment controls must approve the migration mode, rate limiting, workload isolation, audit forwarding and rollback before users can rely on it.

**Next gates:** authenticated application-context session issuance after legacy CAS; limited SQL role and trigger grant checks under PostgreSQL 16; race/cross-process authentication stress; existing-hash inventory; integration of short/master changed paths; owner-approved canonical-repository ADR and independent security signoff. **P0 NO-GO** remains unchanged.

## 7. Verified application-context session bridge — 2026-10-29 ET

The candidate `768e9998b7ea9477ebfa8a8fe22d2699a98b3c91` passed [GitHub Actions #40991023039](https://github.com/danwiz/project0-cardealership/actions/runs/40991023039), **339 tests each on Java 11/17, 0 failures/errors/skips**; the two new `LegacyCredentialApplicationSessionIntegrationTest` cases executed. In both memory and JDBC/H2, a synthetic 120k credential cannot log in through default application authentication. A separately provisioned test migrator verifies, CAS-upgrades to strong 600k and rotates revision; the original application `AuthenticateAccountCommand` then authenticates the newly persisted account through normal `ContextIdentityAdapter` and `RoleAuthorizationService`, while forged roles stay unauthorized. A subsequent password change revokes that session. This is still **not runtime installation of the migration capability or proof of a production role/owner grant**.

The newer isolated candidate `e4a24a588c8faa92cabb6f4ec0c7ca1b463550a3` subsequently passed [CI #40991436945](https://github.com/danwiz/project0-cardealership/actions/runs/40991436945): **341 tests/job**, 0 fail/error/skip, retaining the session bridge while adding two inventory-security regressions.

**Go/no-go:** opt-in source and tests validated; production credential writer provisioning, user-cohort inventory, migration expiry, rate limits, audit, independent review and final canonical-repository promotion remain NO-GO.
