# Car Dealership — cross-branch integration decision register
**Audit date:** 2026-10-29 ET  
**Version:** 1.0 (review draft)  
**Scope:** `danwiz/project0-cardealership` — historical Java console baseline, competing security/modernization stacks and CI-only PostgreSQL purchase proofs.  
**Status:** **P0 integration not accepted / NO-GO for merge, release, migration or deployment.** This document is a review proposal, not merge authorization.  
**Live issue:** [#85 integration governance](https://github.com/danwiz/project0-cardealership/issues/85) and [#89 atomic purchases](https://github.com/danwiz/project0-cardealership/issues/89).

## 1. Evidence boundary and exact immutable heads

| Track | Branch / SHA | Evidence |
| --- | --- | --- |
| Long typed-domain/JDBC stack | `security/postgres-purchase-receipt-reconciliation-20261029` at `bb71cde63b535ce1edd13114995b02bc87b1f2ee` | [Draft #97](https://github.com/danwiz/project0-cardealership/pull/97), [Maven CI #40976704377](https://github.com/danwiz/project0-cardealership/actions/runs/40976704377): Java 11 and 17 success, 315 tests/job, zero fail/error/skip; six PostgreSQL permit/receipt tests |
| Short legacy-console/in-memory authorization stack | `fix/atomic-account-create-20261029` at `086fbf91294f74fe4bd967256498ef94e92c501a` | [Draft #84](https://github.com/danwiz/project0-cardealership/pull/84), synchronization/duplicate-creation behavior; must not be independently merged |
| Long/short common ancestor | `ad8d03574c7f048b236c9d24f0c03ac54dffcbd7` | GitHub Compare API, both directions |
| Long/`master` common ancestor | `9c242f9880a18a7749621a6ed5f6d53d3ee5fcdc` | GitHub Compare API |
| Historic root and alternate branch | #5/#6 shared; long #7–#77 then #86–#97; short #78/#82/#83/#84; docs #46 independent | Open-PR inventory and [issue #85](https://github.com/danwiz/project0-cardealership/issues/85) |

**Counts as inspected:** 86 open draft PRs: 2 common roots, 79 long-stack PRs, 4 short-stack PRs and 1 documentation PR. The prior 75-PR issue text is a historical baseline. Re-query before any release decision.

**Exact compare data:** Long relative to short: 301 ahead, 109 behind; short relative to long: 109 ahead, 301 behind. Tree comparisons list 230 long-differing paths and 25 short-differing paths; **16 path names appear in both direction-specific diffs**. These are neither the number of PRs nor automatically the number of merge conflicts. `master` has 16 commits exclusive to it since its ancestor with the long head, changing CI, password hashing and characterization tests.

## 2. Reviewable decisions (proposed; not yet approved)

| ID | Conflict / capability | Source evidence | Proposed disposition | Non-negotiable test / signoff |
| --- | --- | --- | --- | --- |
| DEC-01 | Authoritative version and historical preservation | Two dealership repositories; Maven repo README claims authoritative modernization, while active transaction development is in legacy-named repo | **Open ADR.** Keep both and original provenance until a named canonical modern target is approved. No renames/history rewrite | Repository graph, origin snapshots, reproducible build, license review |
| DEC-02 | In-memory account creation and update contracts | Long `InMemoryUserAccountRepository` already has synchronized create-only `save`, copy-on-read/write, and conditional `updateCredentialIfCurrent` / `updateRoleIfCurrent`. Short #84 has a shorter synchronized create-only contract | **Retain/adapt long contract** rather than replace it with short implementation. Privileged updates must use authenticated audited service paths | Concurrent duplicate creation; no alias escalation; conditional update; stale account/session rejection |
| DEC-03 | Legacy purchase mutation path | Short `AuthorizedPurchaseReviewService` stages ownership in memory then calls an `Offer` adapter with best-effort compensating rollback | **Do not promote** as JDBC durable transaction; preserve only instructional tests and relevant domain invariants | Stock, ownership, payment and request rollback; no duplicate sale under contention |
| DEC-04 | Configured atomic purchase executor | Long `JdbcPurchaseApprovalService` uses a single SERIALIZABLE JDBC transaction and verified-session gate; #90–#93 cover failure/retry policy | **Candidate foundation**; freeze individual PR promotion until full integration | All mutations single connection/commit, durable request/contract idempotency, correct SQLSTATE behavior, cross-connection concurrency |
| DEC-05 | SQL purchase authority | #94 initial restricted DML; #95 owner-controlled SECURITY DEFINER function with EXECUTE-only writer; #96 issuer-bound expiring one-use permits | **Architectural proof only**. Design authentic isolated permit issuer and writer rather than a fixed CI owner; review function grants/search_path | Deny untrusted writer/reader/table access; prevent minting/forgery/reuse; concurrency, expiry, revocation |
| DEC-06 | Uncertain COMMIT and receipt | #97 adds read-only separate reconciler with COMMITTED, NOT_CONFIRMED and INCONSISTENT | **Adopt the semantics, not a production claim**. Test currently simulates a client exception *after a known successful COMMIT*, not real loss of COMMIT acknowledgment | Actual socket interruption mid-COMMIT, crash/restart, replica lag/failover, read scope, zero double-sell |
| DEC-07 | Role/identity authority | Long `RoleAuthorizationService` validates persisted verified-session state when configured. Short service reauthenticates supplied user credentials for legacy paths | **Explicit server-side identity-bound design**. No client-supplied mutable role or policy-only constructor in privileged runtime | First-admin bootstrap, demotion/deletion, privilege escalation, session invalidation, buyer/reviewer binding |
| DEC-08 | Workflow/CI and `master` drift | CI workflow and six auth/characterization test paths overlap; `master` retains 16 unique commits vs long base | **Reconcile by semantics** before integration candidate. Do not force-push, blanket cherry-pick or import a whole branch blindly | CI event/permission review, Java 11/17 tests, no regression to master PBKDF2 and characterization tests |
| DEC-09 | Independent audits and cloud deployment | Provider-neutral immutable pin/audit documentation exists in long chain, but no proven deployed service or vendor writer authority | **Defer deployment**; require governed migration, independent security/data-integrity review, signed/witnessed audit and measured rollback | Actual environment IAM/grants, secrets/TLS/rotation, retention, incident rollback evidence |

## 3. File-level collision and transplant checklist

The **16 overlapping file paths** that require symbol/behavior-level decisions are:
`.github/workflows/maven-ci.yml`; `src/com/revature/cardealer/{CarDealership,Offer,OwnedVehicle,PaymentPlan}.java`; `src/com/revature/service/{AdminLoginService,CustomerLoginService,EmployeeLoginService,InMemoryUserAccountRepository,UserLoginService}.java`; and tests `CarDealershipCharacterizationTest`, `OfferCharacterizationTest`, `PaymentPlanTest`, `RoleAuthorizationServiceTest`, `RoleLoginServiceCharacterizationTest`, `UserLoginServiceCharacterizationTest`.

**Short-only path candidates requiring test-first evaluation (9):** `docs/ADMIN-BOOTSTRAP-THREAT-MODEL.md`, `docs/PURCHASE-INTEGRITY-REVIEW.md`; `AuthorizedInventoryService.java`, `AuthorizedPurchaseReviewService.java`, `LegacyOfferPurchaseInventoryAdapter.java`, `PurchaseInventoryPort.java`; `CarDealershipRoleRevalidationTest.java`, `AuthorizedInventoryServiceTest.java`, `AuthorizedPurchaseReviewServiceTest.java`.

Specific missing/duplicate behavior to cross-check:
- Deny a copied/forged administrator and revoked/demoted employee in both console and direct application calls.
- Prevent one customer purchase request from assigning inventory/ownership to the reviewer or a different buyer.
- Keep ownership/stock consistent on failures before and after each staged mutation.
- Enforce sold-out single-winner and bounded concurrent-account-creation invariants.
- Apply the long typed-domain `ApplicationPorts.PurchaseApproval` boundary; do **not** silently fall back to short array-backed `Offer` or independent JDBC commits.
- Verify actual legacy menu output; a green isolated port-level test does not prove interactive console safety.

## 4. Go/no-go acceptance evidence

- [ ] Canonical-repository ADR plus immutable source provenance and unmodified legacy artifacts.
- [ ] Full 86-PR dependency ledger, inclusive of all branch head/base SHA and CI evidence; record newly opened PRs before promotion.
- [ ] Written decisions for all 16 overlapping paths and 9 short-only candidates; reviewers sign off on retained/replaced behavior.
- [ ] Reconciled `master`-exclusive 16 commits, including hasher and characterization test fidelity.
- [ ] Reproducible Java 11 and 17 full Maven CI on an **immutable integrated candidate**, with exact run IDs and all tests unskipped.
- [ ] Disposable PostgreSQL 16 security/transaction suite and live process isolation; owner/migrator, issuer, reader, writer, reconciler and auditor independently permissioned.
- [ ] Actual COMMIT acknowledgment-loss chaos test and failover/restart scenarios. A simulated exception after a known COMMIT alone is insufficient.
- [ ] Zero unauthorized role creation, privilege changes, receipt access or purchase writes; reviewer/buyer lifecycle and first-admin bootstrap verified.
- [ ] Real payment ledger reconciliation, recovery/idempotency and no double decrement or double ownership under contention.
- [ ] SQL migration rollback rehearsal, dependency scan with usable feeds, SBOM, sealed evidence hashes, independent security and data-integrity review.
- [ ] Explicit merge/release/deployment authorization, rollback owner and acceptance decision documented.

**Current decision: NO-GO.** The long head is the *comparison baseline and architecture candidate*, not a release candidate. No base-branch modifications, production resources, secret provisioning, changes in repository visibility, or release publication are authorized by this document.

## 5. References

- [Integration tracker #85](https://github.com/danwiz/project0-cardealership/issues/85)
- [Atomic purchase defect #89](https://github.com/danwiz/project0-cardealership/issues/89)
- [Draft #97](https://github.com/danwiz/project0-cardealership/pull/97)
- [Long/short branch comparison](https://github.com/danwiz/project0-cardealership/compare/fix/atomic-account-create-20261029...security/postgres-purchase-receipt-reconciliation-20261029)
- [PostgreSQL 16: CREATE FUNCTION and SECURITY DEFINER](https://www.postgresql.org/docs/16/sql-createfunction.html)
- [GitHub: stacked pull requests](https://docs.github.com/en/pull-requests/get-started/about-stacked-prs)

## 6. Phase 6: updated exact-leaf reconciliation (2026-10-29 ET)

**This section supersedes the earlier #97-leaf counts without altering earlier evidence.** Live GitHub `pulls?state=open&per_page=100` returned **91 PRs, all draft**, with intact head->base relationships:
- **#5 -> #6** = 2 common roots;
- **#7–#77** (68 actual open PRs, not all intervening numeric IDs) followed by **#86–#88, #90–#97, #100–#104** = **84 long-chain PRs**;
- **#78 -> #82 -> #83 -> #84** = 4 competing short-chain PRs;
- **#46** = one independent docs root against `master`.
- Total: **2 + 84 + 4 + 1 = 91**.

New long head [draft #104](https://github.com/danwiz/project0-cardealership/pull/104) = `45eccdc73ce36d4298326498a3603e2363251fd6`. Short head #84 = `086fbf91294f74fe4bd967256498ef94e92c501a`.
- Long vs short: merge-base `ad8d03574c7f048b236c9d24f0c03ac54dffcbd7`; long **341 ahead/109 behind**. Per-direction comparisons show 239 paths on long, 25 on short, **16 path names common**, **9 short-only**. The 16 shared path names are *review surfaces*, **not a computed Git textual conflict count**.
- Long vs `master`: merge-base `9c242f9880a18a7749621a6ed5f6d53d3ee5fcdc`; long **356 ahead/16 behind**. There are **nine `master`-side changed file paths** which must receive distinct parity decisions.

### 6.1 All 16 path-overlap decisions

| File path or abbreviated path under `src/` | Disposition | Acceptance criterion |
| --- | --- | --- |
| `.github/workflows/maven-ci.yml` | **RECONCILE** master/short/long | Keep limited permissions, controlled triggers and Java 11/17+PG16; test on single final candidate; do not break protected branch checks |
| `com/revature/cardealer/CarDealership.java` | **ADAPT** legacy console to verified typed-domain commands | All public entry points require explicit verified actor and permission; old no-actor snapshot operations fail closed |
| `com/revature/cardealer/Offer.java` | **RETAIN long core, TRANSFER tests** | Stable ID/stock and pending-buyer behavior; no double sale, no silently reintroducing mutable arrays |
| `com/revature/cardealer/OwnedVehicle.java` | **RETAIN typed representation** | Ownership immutable with correct buyer/acquisition identifiers |
| `com/revature/cardealer/PaymentPlan.java` | **RETAIN typed plan** | No negative balances, term/price validation and tied transaction/contract IDs |
| `com/revature/service/AdminLoginService.java` | **RETAIN verified bootstrap** | No public unauthenticated first admin or cached-role bypass |
| `com/revature/service/CustomerLoginService.java` | **RETAIN role-scoped registration** | Customer cannot gain reviewer authority via self-registration |
| `com/revature/service/EmployeeLoginService.java` | **RETAIN explicitly trusted employee management** | Role mutations rotate durable session revision; stale actor invalid |
| `com/revature/service/InMemoryUserAccountRepository.java` | **RETAIN latest long version** | Synchronized insert-only creation, defensive copies, conditional credential/role updates, new UUID revision on each mutation/recreate |
| `com/revature/service/UserLoginService.java` | **RETAIN verified-session binding** | Strict username and hash verification, no copied User-object trust |
| `test/java/com/revature/cardealer/CarDealershipCharacterizationTest.java` | **REWRITE expected behavior deliberately** | Historical expected failures retained in archive, current tests assert corrected authorization and safe failure |
| `test/java/com/revature/cardealer/OfferCharacterizationTest.java` | **RECONCILE examples** | Preserve behavioral trace while requiring single-winner and valid request ownership |
| `test/java/com/revature/cardealer/PaymentPlanTest.java` | **COMPARE assertions** | Add only missing plan terms/rounding and negative input tests |
| `test/java/com/revature/service/RoleAuthorizationServiceTest.java` | **COMPARE and augment** | Deny forged admin, demote/re-promote and deletion/recreate; verified revision required |
| `test/java/com/revature/service/RoleLoginServiceCharacterizationTest.java` | **COMPARE and augment** | Existing historical failures documented; no regression to array limits or unsafe user selection |
| `test/java/com/revature/service/UserLoginServiceCharacterizationTest.java` | **COMPARE and augment** | Duplicate create must not overwrite account, authorization epoch and defensive views preserved |

### 6.2 The nine short-only paths

| Exact source-relative path | Proposed action | Status |
| --- | --- | --- |
| `docs/ADMIN-BOOTSTRAP-THREAT-MODEL.md` | **Evidence migration**: compare trust assumptions with long `docs/security/administrator-bootstrap.md`; copy/annotate useful scenarios, no wholesale overwrite | Review pending |
| `docs/PURCHASE-INTEGRITY-REVIEW.md` | **Evidence migration**: crosswalk against #89 SQL permit/receipt failure model | Review pending |
| `src/com/revature/service/AuthorizedInventoryService.java` | **Do not transplant** duplicate legacy privilege/mutation service; map behavior to `ManageInventoryCommand` and tested context adapter | Covered partly by #100; parity review pending |
| `src/com/revature/service/AuthorizedPurchaseReviewService.java` | **Do not transplant** in-memory best-effort compensation as production authority; map invariants to single JDBC transaction | Functional parity review pending |
| `src/com/revature/service/LegacyOfferPurchaseInventoryAdapter.java` | **Defer to archive** with provenance until full console parity | Not approved for production |
| `src/com/revature/service/PurchaseInventoryPort.java` | **Defer/reconcile port contract**, avoid parallel competing interfaces | Review pending |
| `src/test/java/com/revature/cardealer/CarDealershipRoleRevalidationTest.java` | **Test-only transfer by behavior**: null/missing admin, forged admin, deleted admin, direct save/load denial | Partly reflected in #98/#99; explicit parity check required |
| `src/test/java/com/revature/service/AuthorizedInventoryServiceTest.java` | **Test-only transfer by behavior**: valid staff add, customer/forged/revoked/demoted denied, unchanged inventory | #100 tests demotion in memory + JDBC/H2; other cases require coverage check |
| `src/test/java/com/revature/service/AuthorizedPurchaseReviewServiceTest.java` | **Test-only transfer by behavior**: buyer attribution, missing buyer, rollback, one-stock competition, input validation | #89/#90/#104 cover important typed/JDBC scenarios; remaining legacy console parity requires review |

### 6.3 Nine `master`-side changed paths — separate security and historical baseline gate

| Changed path on `master` (compared with long #104 head) | Required disposition |
| --- | --- |
| `.github/workflows/maven-ci.yml` | **RECONCILE** event/protection semantics, not blindly replace CI workflows |
| `src/com/revature/service/Pbkdf2PasswordHasher.java` | **P0 BLOCKER**: master default **600,000** HMAC-SHA256 iterations, verification cap **2,000,000**, encoded length max **512**, 16-byte salt and 256-bit output; long uses **120,000** new hashes with unbounded verifier work factor and key length derived from attacker-controllable encoding. Preserve stronger master security semantics and design bounded legacy-hash migration |
| `src/test/java/com/revature/service/Pbkdf2PasswordHasherTest.java` | **P0 TEST PARITY**: preserve master `rejectsUntrustedWorkFactorsBeforeHashing`; test malformed/oversized encoded input before PBKDF2 and no downgrade of new hashes |
| `src/test/java/com/revature/DAOService/DAOServiceCharacterizationTest.java` | Preserve historical file behavior as evidence, enforce modern no-actor access and safe deserialization in current app |
| `src/test/java/com/revature/cardealer/CarDealershipCharacterizationTest.java` | Preserve original failure cases in archive; current corrected console requires fail-closed snapshot and role boundary |
| `src/test/java/com/revature/cardealer/OfferCharacterizationTest.java` | Preserve historical behavior trace while requiring stable inventory/pending-request logic |
| `src/test/java/com/revature/cardealer/PaymentsCharacterizationTest.java` | Preserve historical fixed-capacity/balance failures in archive; modern financial ledger invariants required |
| `src/test/java/com/revature/service/RoleLoginServiceCharacterizationTest.java` | Preserve provenance; explicit signed-off migration from historical fixed-array cases |
| `src/test/java/com/revature/service/UserLoginServiceCharacterizationTest.java` | Preserve historical registration and delete cases; ensure modern unauthorized deletion remains denied |

**Security note:** The PBKDF2 issue is verified by direct source comparison, **not by exploitation of a deployed service**. It is a clear potential regression on combining these heads. OWASP's current PBKDF2-HMAC-SHA256 recommendation is 600,000 iterations or more (when PBKDF2 is used), with work factors tuned and rehashed safely: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

### 6.4 Release candidate integration order — no destructive steps

1. **Approve ADR**: [canonical repository proposal](ADR-CAR-DEALERSHIP-CANONICAL-REPOSITORY-2026-10-29.md). The Maven repo's own README designates it canonical, but the active 91-PR stack is in the other repository.
2. **Freeze heads**: latest #104, #84, `master`, Maven `master`, #46 and source history; record SHA, license, original artifact checksums.
3. **Reconcile `master` first**: carry forward stricter PBKDF2 and master characterization evidence; do not accidentally ship 120k new hashes or unbounded encoded hash verification. Define bounded legacy credential migration or rehash-on-login without locking out existing accounts.
4. **Reconcile short branch by behavior**, not by merging the best-effort in-memory purchase service: make a coverage table for the 6+5+10 short-only test cases against long/JDBC test classes; only add missing tests.
5. **Create one integration candidate** only after P0 design review, preserving all branches and `master`; don't force-push or merge a leaf PR into `master`.
6. **Run full exact-SHA validation**: Java 11 and 17, PG16 grants/migration, TX-01–TX-15, negative account/session/reviewer tests, dependency verification and SBOM; reproduce test logs outside source branches.
7. **Approve promotion** only with independent DBA/security/maintainer review, correct provenance, explicit rollback strategy and signed acceptance record.

**Current integrated-release decision: NO-GO.** No branch merges, rewrites, default-branch changes or releases performed by this register.

## Phase 10 — master-side reconciliation checkpoint (2026-10-29 ET)

- **Actual protected baseline:** `master` commit `90741d3abe51d9cc002aaeb1dacae27b933fba10`, captured with [exact nine-file blob and original-test manifest](CAR-DEALERSHIP-MASTER-BASELINE-PRESERVATION-MANIFEST-2026-10-29.md). Historical tests from six changed `master` characterization suites document deliberately defective legacy behavior and should be treated as immutable **pre-remediation evidence**, not pasted into modern tests expecting those bugs.
- **Two files now byte-equivalent to master:** `Pbkdf2PasswordHasher.java` blob `fe47ab27572523fa1047443c4090ed758891e5c5` and `Pbkdf2PasswordHasherTest.java` blob `ceec0a5db502d597b5626775bdc6463194b9703e`. Verified via two independent `fetch_file` reads, not inferred from test counts.
- **Workflow semantic drift resolved on candidate:** the modern `maven-ci.yml` omitted the protected `master` push trigger and master-only diagnostics matrix. These were copied into the existing Java 11/17 + disposable PG16 workflow at isolated candidate commit `0cbad314956ad1d36542d30afa6519a1bbfecdce`, without touching the actual protected `master`. CI [#40997446982](https://github.com/danwiz/project0-cardealership/actions/runs/40997446982) was **not yet complete** when recorded. On completion, inspect both verify jobs and both diagnostics jobs, artifact fetch and test totals before calling this step validated.
- **No automatic conflict resolution:** 16 `master`-exclusive commits and four short-branch PRs remain history from separate lines. This is a reviewed functional/provenance disposition, **not a Git merge, accepted canonical Maven migration, or authorization to publish**.

**Owner/DBA/security approval and the broader release NO-GO are unchanged.**
