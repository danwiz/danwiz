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
