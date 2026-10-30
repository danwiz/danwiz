# PostgreSQL Purchase Integrity — Failure-Mode & Acceptance Matrix
**Date:** 2026-10-29 ET  
**Scope:** `danwiz/project0-cardealership`  
**Status:** DRAFT / P0 RELEASE NO-GO — evidence ledger, not a deployment approval.  
**Tracks:** [#89 atomic purchases](https://github.com/danwiz/project0-cardealership/issues/89), [#85 long/short integration](https://github.com/danwiz/project0-cardealership/issues/85).

## Baseline and immutable CI record

| Stack | Head SHA | Latest relevant evidence | Status |
| --- | --- | --- | --- |
| Durable session revocation | `b3cb317205ec3e9c4c7515383ecff70626bf2ff1` | [#101 / run 40981527980](https://github.com/danwiz/project0-cardealership/actions/runs/40981527980); Java 11/17 each 322 tests, 0 fail/error/skip; PostgreSQL16 migration exercised | Draft CI-verified, not approved |
| Authorized legacy snapshot boundary | `c43438003fe094f46e207611ac2939e8f7be3f1c` | [#102 / run 40982696721](https://github.com/danwiz/project0-cardealership/actions/runs/40982696721); Java 11/17 each 327 tests, 0 fail/error/skip | Draft CI-verified, not approved |
| Transaction-bound reviewer revision | `d56d9ec76fb12432bab3bc2b875302874f2ee373` | [#103 / run 40983209417](https://github.com/danwiz/project0-cardealership/actions/runs/40983209417); Java 11/17 each 328 tests, 0 fail/error/skip | Draft CI-verified, not approved |
| Real PostgreSQL **before/after COMMIT TCP loss** | `45eccdc73ce36d4298326498a3603e2363251fd6` | [#104 / run 40985413694](https://github.com/danwiz/project0-cardealership/actions/runs/40985413694); Java 11/17 each **330** tests, 0 fail/error/skip; two actual transport-cut tests non-skipped | Draft CI-verified, not approved |

All of these are **stacked draft branches**. Passing CI does not imply they were integrated into `master` or the separately named Maven modernization repository. The profile audit remains draft.

## Test / threat matrix

| ID | Failure or attacker case | Current evidence | Status | Required next acceptance |
| --- | --- | --- | --- | --- |
| TX-01 | SQL failure after stock/request/ownership/plan mutation | `JdbcPurchaseApprovalServiceTest` injected-stage rollbacks; disposable PostgreSQL ownership-insert rollback | **Tested** | Repeat under exact integrated candidate and immutable schema |
| TX-02 | Serializable conflict / deadlock 40001/40P01 | `JdbcPurchaseRetryPolicyTest` bounded whole-transaction retries | **Tested in CI** | Workload/lock contention on actual PostgreSQL connections |
| TX-03 | Unknown SQLSTATE 08006/40003 | Existing `JdbcPurchaseRetryPolicyTest` SQL exception injection | **Simulated** | Real transport disruption cases |
| TX-04 | Response loss **after server COMMIT completes** | #104 actual local TCP relay; intercepts backend ReadyForQuery and cuts client before acknowledgement; independent PostgreSQL readback shows one complete sale | **Actual TCP cut, tested in isolated PG16** | Additional runs under monitored network jitter, process restart and proof of no auto-write replay |
| TX-05 | Connection lost **before COMMIT reaches server** | #104 actual TCP proxy discards outbound COMMIT and closes socket; independent PG16 readback: request PENDING, stock unchanged, no ownership/payment plan; JDBC reports unknown outcome without retry | **Actual TCP cut, CI-tested on exact #104 head** | Production SQL permit-receipt NOT_CONFIRMED semantics, competing-writer races, independent reviewer signoff |
| TX-06 | Connection cut **during** COMMIT processing / ambiguous backend crash | Not established by #104, which cuts *after* ReadyForQuery | **Untested** | At least two fault placements and independently verified recovery without second sale |
| TX-07 | PostgreSQL primary failure, crash/restart, WAL replay and standby promotion | No independently verified physical failover evidence | **Untested** | Real container/process failure rehearsal, persistence checks, RPO/RTO and durable receipt proof |
| TX-08 | Wrong/corrupt payment-plan or ownership state | SQL permit receipt test detects `INCONSISTENT` when operator corrupts price | **CI proof** | Cross-table and external payment-ledger reconciliation; read-only signed audit |
| TX-09 | Permit forged/expired/revoked/replayed | `PostgresqlPurchasePermitBoundaryTest` owner, issuer, restricted writer/reader checks | **CI-only SQL proof** | Real process-specific authentication, credential custody, scoped permit minting and revocation |
| TX-10 | Receipt read with unknown token, wrong request/terms or unauthorized identity | SQL `SECURITY DEFINER` receipt tests, COMMITTED/NOT_CONFIRMED/INCONSISTENT | **CI-only SQL proof** | Authenticated API, rate limit, audit, projection/data minimization |
| TX-11 | Replica lag / stale read shows NOT_CONFIRMED while primary has committed | Not physically exercised | **Untested** | Primary-authoritative or consistency-fenced read; never use NOT_CONFIRMED as permission for automated retry |
| TX-12 | Reviewer demoted then re-promoted after Java check but before DB row lock | #103 deterministic ABA test + persisted session_revision recheck under `FOR UPDATE` | **CI-tested in H2/JDBC** | PostgreSQL cross-process concurrency stress, least-privilege role checks |
| TX-13 | Double buyer / one remaining stock unit | Existing H2 and PostgreSQL simultaneous-purchase tests | **CI-tested** | Load/stress in isolated staging against exact release candidate |
| TX-14 | Historical short/long branch conflict, unique master commits and authoritativeness | #85 dependency graph, 16 overlapping paths, 16 master-exclusive commits | **Analysis only** | Canonical repository ADR, 86+ PR decision ledger, signed code review, merged integration branch |
| TX-15 | Malicious/untrusted historical Java file deserialization | #102 bounded JDK ObjectInputFilter and no-actor access guards | **CI-tested for narrow fixtures** | Offline archive migration, signed data-only format, atomic writes/fsync, symlink/TOCTOU/permissions review |


## TX-05 verification addendum — October 29, 2026 ET

- **Immutable head** `45eccdc73ce36d4298326498a3603e2363251fd6`; [GitHub Actions #40985413694](https://github.com/danwiz/project0-cardealership/actions/runs/40985413694) **COMPLETED SUCCESS** with **330 tests each** on Java 11 and Java 17; zero fail/error/skip.
- Both CI job logs show two non-skipped `PostgresqlCommitAckTransportLossTest` cases running in test and verify phases.
- **TX-04**: real COMMIT forwarded; ReadyForQuery withheld from client; a single durable purchase confirmed on a separate connection.
- **TX-05**: real outbound COMMIT bytes not forwarded; sockets closed; caller reports unknown transport outcome; *independent PostgreSQL query* confirms PENDING request, stock still 2, zero ownership and payment plans. This test does not query the separately protected SQL receipt function or claim general exactly-once guarantees.
- The proxy requires strict isolated CI PostgreSQL 16 environment, uses a random schema, and does not deploy or require any production credential. The test-only connection intentionally disables SSL to observe protocol frames; production must use authenticated TLS transport.
- **Remaining P0 risks**: in-flight commit/backend crash, primary failover/replica promotion, stale reads, independent issuer/writer/reconciler integration, complete external payment-ledger audit, and #85 cross-branch integration. Issue #89 stays open; no PR merged or released.

## Safe post-error reconciliation policy

1. **Do not auto-retry** an approval after SQLSTATE 08*, 40003 or unknown COMMIT outcome (including the physically tested pre-COMMIT client cut). Never substitute a second request ID, a new permit or fresh payment terms to force success.
2. Record the original immutable request ID, original permit/contract ID where applicable, authenticated actor, operation parameters, exact release SHA, failure timestamp and nondisclosing diagnostic correlation ID. Do not log credentials or bearer tokens.
3. Query the **independently authorized, read-only, primary-consistent** receipt interface if provisioned. If not provisioned, require a trained authorized operator using direct SQL readback; the Java JDBC test's direct reader is a CI fixture, **not** a production reconciliation API.
4. `COMMITTED` requires consistent request, buyer, stock/ownership/payment terms and durable evidence. Return the original purchase receipt with no new write.
5. `NOT_CONFIRMED` means no durable confirmation *at that observation point* — **not** approval to retry. Another in-flight commit or stale replica could change the answer. Re-authorize only under a separately reviewed idempotent operation protocol and lock.
6. `INCONSISTENT`, unknown, stale or contradictory evidence -> block writes, preserve evidence, alert incident owner, independently investigate.
7. Do not claim exactly-once purchase semantics until **TX-06, TX-07 and TX-11** and the production issuer, writer and reconciler service identity boundaries pass independent review. TX-05 is isolated CI-verified, not a production recovery protocol.

## Acceptance ownership

| Required decision | Suggested accountable reviewer | Evidence to collect |
| --- | --- | --- |
| Canonical release source / preservation | Repository maintainer and architecture owner | Signed ADR, source provenance and branch dependency ledger |
| Database privilege/function migration | DBA/security reviewer independent of code author | Owner/grant diff, function search_path, schema verification and rollback proof |
| Failure-injection and recovery | Independent QA/SRE reviewer | Actual network/proxy transcripts, backend log, exact SHA, CI artifact and DB readback |
| Payment correctness | Domain/finance controls reviewer | Ledger reconciliation, single ownership and no double inventory consumption |
| Release | Authorized repository owner | Exact-candidate green CI, reproducible build, SBOM and explicit no-go closure record |

## Next actionable work

- **TX-05 implemented and verified**: retained the existing draft PR #104 and confirmed the outbound COMMIT is intercepted before PostgreSQL receives it, with independent PENDING/unchanged-row readback. The SQL permit/receipt function was *not* used in this test, so no integrated NOT_CONFIRMED receipt claim.
- Exercise TX-06 and TX-07 using an isolated backend process/container lifecycle, with receipt and transaction logs retained.
- Wire read-only reconciliation and authentically isolated issuer/writer roles into a reviewable Java runtime candidate, *without* provisioning production services.
- Reconcile competing long/short dealership PR stacks (#85), and complete Project1's vulnerability report before reclassifying the overall portfolio maturity.

**This document authorizes no default-branch merges, production schema changes, external provisioning, credential rotation or published release.**
