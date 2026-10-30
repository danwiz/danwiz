# GitHub portfolio remediation plan — baseline 2026-10-29

**Original discovery snapshot:** 18 personal repositories and 22 issues in 6 repositories (the counts below describe that earlier report and remain historical).  
**Reverified 2026-10-29 (ET):** **21 accessible repositories** (18 personally owned, 2 Wisdom Technologies organization-owned, 1 collaborator-owned); **30 open issues across 8 repositories** and **110 open PRs**. Individual repository searches were necessary: an earlier multi-repository search returned only 13 issues in two repositories, thereby omitting 17 open issues from six additional repositories. The 30 total is: Car Dealership 7, Project1 6, profile 7, IT Readiness Toolkit 3, Project Intelligence Agent 2, PRJ-ERM-001 2, CMF-SE 3; other 13 repositories 0. PR distribution: Dealership 86, Project1 21, Toolkit 2, profile 1. **Do not treat original 22-issue sections below as a complete current register.**  
**P0 integration supplement:** [Car Dealership cross-branch decision register](CAR-DEALERSHIP-INTEGRATION-DECISION-REGISTER-2026-10-29.md) and [integration issue #85](https://github.com/danwiz/project0-cardealership/issues/85). Exact long-vs-short head divergence: 301 vs 109 exclusive commits, with 16 overlapping changed paths; `master` has 16 branch-exclusive commits relative to the long head's common ancestor. Keep both branches draft and unmerged. This is a discovery/control baseline, **not** a declaration of comprehensive source, workflow, or security verification. Do not merge, deploy, archive, or delete historical repositories on the strength of this plan.

## Repository inventory and lifecycle classification

| Repository | Category / purpose | Observed features and options | Provisional lifecycle | Evidence / next verification |
| --- | --- | --- | --- | --- |
| danwiz | Personal brand and portfolio | Profile README, links, branding, Pages | Portfolio development | Issues #1-4, #16-17, #24; check Pages, metadata, links, pins |
| project0-cardealership | Java dealership domain app | Accounts, role-based permissions, inventory, offers, purchases, ownership, payments | Development / security-blocked integration | Issues #25, #29, #79-81; draft PR #82; Java 11/17 tests |
| Project0-Cardealership-Maven | Java/Maven dealership modernization | Console, login, inventory, offers, file persistence | Legacy modernization | Verify relationship to project0-cardealership, license, tests and releases |
| Project1 (private) | Training/software project; purpose unconfirmed | Requires manifest and source inventory | Discovery / unclassified | No README on default branch; inspect source |
| RevatureiOS (private) | iOS training | Source and targets require inspection | Training / discovery | No README on default branch; inspect Xcode project |
| HOL5 | Training lab | Scope undocumented | Training / documentation | README only '# HOL5'; inspect contents |
| UIPageViewController-Post | Swift UI example | Page-view-controller tutorial | Reference / learning | Verify build and attribution |
| AppAuth-iOS | External iOS auth SDK | OAuth 2.0 / OIDC | External reference | Audit upstream, license, fork status and security |
| auth0-ios-swift-sample | External iOS authentication example | Auth0 quickstart | External sample | Verify provenance, secrets, build |
| ioscreator | iOS tutorial examples | Swift/iOS samples | External reference / legacy | Verify ownership, attribution, obsolete APIs |
| Alamofire | External Swift networking SDK | HTTP networking | External reference | Verify fork/upstream, licensing, vulnerabilities |
| wisdom-it-readiness-toolkit | Python consulting assessment tool | Weighted scoring, maturity levels, JSON/Markdown reports, CI | Released v0.1.0 / development | Issues #5, #9-10; assess release evidence |
| sports-management-system-legacy | Preserved C++ coursework + modernization | Legacy preservation, C++20 modernization | Released v0.11.0 / modernization | Validate release assets, build, Pages and provenance |
| wisdom-project-intelligence-agent (private) | AI-assisted project evidence analysis | Python, Pydantic, read-only synthesis, auth adapters | Development / CI blocked | Issues #4-5; inspect Actions and WIF |
| oop-desk-mat-reference-model (private) | OOP reference documentation/model | Scope requires source inspection | Research / discovery | No README; inspect assets |
| cmp1025-programming-2 | Java instructional baseline | Java 21, Maven, JUnit, ArchUnit, JaCoCo, quality gates | Released v0.9.0 / instructional | Validate release, dependency alerts, CI |
| prj-erm-001-reference-implementation (private) | C#/.NET enterprise reference system | APIs, EF Core, PostgreSQL, Docker, requirements traceability | Integration / security blocked | Issues #19, #24; .NET lifecycle, Trivy, CodeQL availability, stacked PRs |
| cmf-se-case-model-framework (private) | Case-model engineering framework | ER/EER/UML, Gherkin, traceability | Framework development / governance | Issues #2-4; branch rules, diagrams, dependency inventory |

**Lifecycle meanings:** Discovery = identity/source unverified; Research = conceptual assets; Development = actively changing; Testing = verification underway; Staging = separately deployed pre-production environment evidenced; Production = operational deployment and release governance evidenced. Releases and passing CI alone do not establish staging or production.

## Open issue workstreams (22 issues)

- **Profile / danwiz (7):** #1 account metadata and Pages; #2 IT Readiness Toolkit launch; #3 profile metadata/Pages; #4 Sports Management publication; #16 portfolio audit; #17 CMP1024 authoritative repo; #24 cross-portfolio P0/P1 remediation control.
- **Car Dealership (5):** #25 portfolio modernization; #29 forged roles and privileged self-registration; #79 offer indexing, atomicity and durable purchase consistency; #80 trusted one-time admin bootstrap; #81 owned-car null dereference and browse/purchase separation.
- **PRJ-ERM-001 (2):** #19 baseline CI, observability and legal-hold migration conflicts; #24 Trivy container vulnerabilities, .NET 9 lifecycle and release-security evidence.
- **CMF-SE (3):** #2 private main branch protection; #3 bookstore ER/EER/UML semantics; #4 dependency inventory, alerts and private security-policy visibility.
- **AI Project Agent (2):** #4 GitHub Actions workload identity federation; #5 Actions/CI/CodeQL visibility.
- **IT Readiness Toolkit (3):** #5 v0.2.0 planning; #9 richer reports/release validation/case study; #10 governed README.

## Remediation priority and planned solution

### P0 — Security, integrity, release blockers
1. **Car Dealership:** prohibit unauthenticated staff/admin registration; bind authorization to persisted authenticated principals; establish one-time trusted bootstrap with no default secrets; verify negative role-escalation tests. Keep draft PRs unmerged until integrated security tests pass.
2. **Car Dealership purchase integrity:** complete repository-wide direct-call inventory for public Offer.setAccept; route all production purchase decisions through PurchaseInventoryPort; preserve characterization tests; add durable transaction design for inventory decrement + ownership + payment obligation + idempotency key + audit event in one database transaction. Verify concurrency, retry, crash recovery, and rollback. Current in-memory rollback and adapter are NOT ACID.
3. **PRJ-ERM-001:** establish eligible CodeQL/dependency-review security scanning or an explicitly reviewed alternative evidence workflow; address critical/high Trivy findings, .NET 9 lifecycle, legal-hold migrations; fail closed on missing evidence. Do not silently waive required controls.
4. **Secrets/provenance:** scan repositories and GitHub Actions permissions; review third-party SDK provenance and licenses; no destructive rewrite without preservation plan.

### P1 — Reliability and governance
5. Resolve Car Dealership owned-vehicle null dereference and decouple browsing from purchase requests; run Java 11/17 CI.
6. Fix AI-agent Actions status and WIF trust boundaries; use least-privilege short-lived credentials.
7. Apply eligible branch protection/rulesets, CODEOWNERS, SECURITY.md, dependency inventory, release policies and diagram review to CMF-SE and other owned projects.
8. Review default branch vs stacked draft PRs, required checks, workflow logs, releases, tags, and dependency lifecycle across all 18 repositories. Track verified results per repo.

### P2 — Portfolio and presentation
9. Confirm profile README, metadata, pinned repositories, Pages, links, licensing, attribution and accessible case studies.
10. Complete governed README and v0.2.0 roadmap for IT Readiness Toolkit; validate Sports Management v0.11.0 assets; audit CMP1025 baseline; determine CMP1024 source provenance.
11. Classify external reference/fork repositories separately from original authored portfolio work. Do not claim third-party SDK authorship.

## Per-repository audit checklist

Record: repository identity and ownership; purpose; README and architecture; source and language/build manifests; features; data/security boundaries; license/provenance; dependency and secret scans; Actions and status checks; issues/PRs; release/tag/assets; Pages/deployments; environment evidence; tests and coverage; maintainers; risks; severity; proposed repair; acceptance tests; verified lifecycle stage. Mark each finding **verified**, **inferred**, or **unknown** and link evidence.

## Execution and closure gates

**Phase 0:** capture immutable inventory, issues, branches, PR stack, CI/release evidence; avoid rewriting historical artifacts.

**Phase 1:** resolve P0 defects in draft PRs with test evidence, independent review, and documented residual risk.

**Phase 2:** stabilize P1 CI, branch rules, security posture, and dependency management.

**Phase 3:** complete P2 README/portfolio/Pages/release hygiene.

**Phase 4:** re-audit all 18 repositories and all originally open issues. Close an issue only when its acceptance criteria are met and linked evidence is verified; track blockers separately.

**Go/no-go:** Resume GitHub Ecosystem Setup only after P0 blockers are resolved or explicitly accepted under documented governance; no security-control bypass, no unaudited merge, no unsupported production claims.

## Provenance audit supplement — 2026-10-29

The following observations are from actual default-branch files; they establish source attribution, **not** fork metadata or the presence/absence of original contributions:

| Repository | Source evidence | Required action |
| --- | --- | --- |
| Project0-Cardealership-Maven | README calls it the authoritative Java modernization target; Maven artifact `com.revature:cardealer:0.1.0-SNAPSHOT` | Reconcile with separate legacy dealership repository before consolidation |
| Project1 | Maven `com.revature.superhuman:SuperHuman:0.0.1-SNAPSHOT`, WAR packaging | Inspect web endpoints, PostgreSQL use, tests, deployment and credentials |
| RevatureiOS | Root README and license not found at inspected paths | Inspect Xcode project and source history; do not infer no license elsewhere |
| HOL5 | Root README contains only `# HOL5` | Determine lab scope and build targets |
| UIPageViewController-Post | README explicitly links Atomic Object Swift tutorial | Verify attribution and original modifications |
| AppAuth-iOS | README identifies OpenID AppAuth SDK; Apache 2.0 LICENSE present | Verify upstream fork relation and local changes |
| auth0-ios-swift-sample | README links Auth0 native iOS Swift quickstart; MIT license credits Auth0 Samples | Preserve Auth0 attribution; review sample configuration |
| ioscreator | README identifies ioscreator.com tutorials, updated 2020 | Treat as external tutorial collection pending contribution audit |
| Alamofire | README links upstream Alamofire SDK; LICENSE credits Alamofire Software Foundation | Preserve MIT license and upstream credit; inspect local changes |

**Release-evidence supplement:** `wisdom-it-readiness-toolkit` README identifies published v0.1.0 while `pyproject.toml` declares `0.2.0.dev0`; CI includes Python 3.11 installed CLI tests. `sports-management-system-legacy` README identifies v0.11.0, seven tests and CPack ZIP/TGZ, still requiring independent release-asset verification. `cmp1025-programming-2` declares Java 21/Maven artifact version 0.9.0 and CI runs Spotless/tests/verify. Latest-commit workflow lookups for these three returned no runs, an inconclusive result rather than CI failure.

**Audit status:** Source attribution and selected manifests verified; full source diff, workflow history, deployment, and release-asset audit remain open. Do not automatically claim third-party source as original authorship or archive/delete it.


## Phase 1 source-security update — 2026-10-29 ET (later checkpoint)

**Current checked totals:** 21 accessible repositories, **32 open issues** across 8 issue-bearing repositories, and **111 open pull requests** (87 Car Dealership, 21 Project1, 2 IT Readiness Toolkit, 1 profile). The earlier 30-issue/110-PR and 22-issue/75-PR counts remain historical snapshots; **do not substitute them for these newer counts**. The two new Car Dealership issues are [#98 stale verified-session reactivation risk](https://github.com/danwiz/project0-cardealership/issues/98) (P0, source-level hypothesis requiring CI reproduction) and [#99 direct snapshot persistence authorization / Java deserialization](https://github.com/danwiz/project0-cardealership/issues/99) (P1, local in-process trust-boundary issue, no remote exploit established).

**Executed GitHub actions:** Added a test-only, unmerged, stacked [draft PR #100](https://github.com/danwiz/project0-cardealership/pull/100), head `54b2757f753a5cba23942e63817a7b97a9659c3b`, based on draft #97; it covers configured in-memory and JDBC/H2 **immediate demotion** denying unauthorized inventory add/remove. It **does not** solve irreversible demote-and-restore revocation. CI run [#40979720669](https://github.com/danwiz/project0-cardealership/actions/runs/40979720669) **COMPLETED SUCCESS** on exact head: Java 11 and Java 17 each passed **317 tests, zero failures/errors/skips**. Both job logs confirm the two new `SessionDemotionInventoryRegressionTest` cases executed (0 failures/errors/skips). This is test-only coverage, **not** a fix for P0 #98 or approval to merge. [Issue #85 comment](https://github.com/danwiz/project0-cardealership/issues/85#issuecomment-6511832392) holds full trace.

**Project1 security verdict remains unavailable:** Dependency-Check 12.2.2 under Temurin JDK17 at draft #27 head `229d0401843fbe4c4e293787493976d39259ac5f` reported 416,766 NVD entries without an API key, then [audit run #40952531972](https://github.com/danwiz/Project1/actions/runs/40952531972) ended CANCELLED after approximately 35 minutes with no nonempty JSON/HTML report and no artifact. Timeout was configured at 35 minutes; cause needs verification. Successful Java 8 Maven/SBOM/DB checks **do not provide a vulnerability verdict**. See [Project1 #26 evidence comment](https://github.com/danwiz/Project1/issues/26#issuecomment-6511833267).

**Disposition:** All integration and production gates remain NO-GO. Do not merge source stacks or treat documentation/test-only PRs as a completed fix.


## Phase 2 security remediation — draft #101 (2026-10-29 ET)

**Live checked inventory at this checkpoint:** 21 accessible repositories, 32 open issues, **112 open PRs** (88 Car Dealership, 21 Project1, 2 IT Readiness Toolkit, 1 profile). These totals supersede the earlier historical figures in this audit; no issues have been closed and no PRs have been merged by this work.

**P0 #98 scoped implementation:** [Car Dealership draft PR #101](https://github.com/danwiz/project0-cardealership/pull/101), stacked on #100, adds an opaque server-issued account session revision and invalidates old verified sessions after role/credential mutation, demote-and-restore, and account deletion/recreation. Schema v5 adds PostgreSQL and H2 UUID defaults and a PostgreSQL owner-controlled BEFORE UPDATE trigger (narrow credential-only SQL writers remain without UPDATE rights on the revision). Includes four H2/memory regressions and one disposable PostgreSQL 16 migration/rollback/security test. [Design and recovery conditions](https://github.com/danwiz/project0-cardealership/blob/security/durable-session-revocation-20261029/docs/security/account-session-revocation-generation.md).

**Evidence must be tracked, not assumed:** [Initial CI run #40980400193](https://github.com/danwiz/project0-cardealership/actions/runs/40980400193) failed (four new revocation tests succeeded; legacy JDBC projection, SQL column privileges and schema-version tests failed). The implementation was adjusted to avoid broad SQL grants, and exact-head [follow-up CI #40980966771](https://github.com/danwiz/project0-cardealership/actions/runs/40980966771) was QUEUED when this entry was written. A clean verdict is **not yet established**. See [issue #98 verification note](https://github.com/danwiz/project0-cardealership/issues/98#issuecomment-6511997225).

**Remaining P0 no-go:** live process identity and SQL role isolation, actual COMMIT-loss/failover tests, transaction-bound authorization and short/long branch integration. Do not merge, run production schema migrations, deploy or publish a release from this draft.


## Phase 2 verified CI checkpoint — draft #101 (2026-10-29 ET)

**P0 #98 test-candidate evidence confirmed:** [Car Dealership draft PR #101](https://github.com/danwiz/project0-cardealership/pull/101), immutable head `b3cb317205ec3e9c4c7515383ecff70626bf2ff1`, passed [Maven CI #40981527980](https://github.com/danwiz/project0-cardealership/actions/runs/40981527980). Java **11 and 17 each passed 322 tests, zero failures/errors/skips**, with successful package verification. Both job logs confirm **4 session revocation regression tests** and **1 disposable PostgreSQL 16 v4-to-v5 migration/owner-trigger test** actually executed and were not skipped.

The fix uses a durable owner-generated account session revision for fail-closed old-session matching; the PostgreSQL owner-trigger rotates it even for constrained credential-only SQL writers without expanding their UPDATE privileges. H2 and in-memory use separate compatible local behavior. Early candidate CI runs failed due to initial schema/grant/fixture issues, which were corrected and retested rather than bypassed. [#98 verification record](https://github.com/danwiz/project0-cardealership/issues/98#issuecomment-6512112341).

**Status:** P0 #98 is **draft-code/test verified** but not production-approved or closed. DB migration/provisioning, independent security review, #85 cross-branch integration, #89 atomic purchase authority/commit-loss testing, #99 snapshot permissions and Project1 vulnerability-verdict gaps remain blockers. Keep the PR draft; no merging or deployment. Inventory at this checkpoint: 21 repositories, 32 open issues, 112 open PRs.


## Phase 3 security checkpoint — snapshot authorization, draft #102 (2026-10-29 ET)

**Current verified portfolio totals:** 21 accessible repositories, **32 open issues**, **113 open PRs** (89 Car Dealership, 21 Project1, 2 IT Readiness Toolkit, 1 profile). Prior counts are historical baselines, not current.

**P1 issue #99 implemented and branch CI-verified:** [Car Dealership draft #102](https://github.com/danwiz/project0-cardealership/pull/102) is stacked on #101; exact head `c43438003fe094f46e207611ac2939e8f7be3f1c` passed [Maven CI #40982696721](https://github.com/danwiz/project0-cardealership/actions/runs/40982696721): Java 11 and 17 **327 tests each, no failures, errors or skips**, package BUILD SUCCESS. Logs explicitly show `SnapshotAuthorizationBoundaryTest` (1 test), `DAOServiceSecurityTest` (4 tests), existing DAOService characterization (4 tests), and existing PostgreSQL16 schema v5 migration tests (1 test) all executed and passed.

Candidate behavior: application save/load commands, persistence adapter and context require currently verified administrator and the exact `CarDealer.dat` name; no-actor entry points fail closed. A local JDK object filter with bounded file size, graph metrics and explicit class allowlist protects historical Java snapshot reads, rejecting unknown classes and symlinks while preserving tested roundtrip. [Issue #99 exact-head evidence](https://github.com/danwiz/project0-cardealership/issues/99#issuecomment-6512267220) and [legacy snapshot threat model](https://github.com/danwiz/project0-cardealership/blob/security/authorized-snapshot-boundary-20261029/docs/security/legacy-snapshot-persistence-security.md).

**NO-GO remains:** Filesystem race, archive integrity, atomic write, real historical-archive migration and independent security signoff remain incomplete. #85 branch reconciliation, #89 purchase-atomicity and authentic COMMIT-loss tests, #98 independent production schema migration review, and Project1 vulnerability audit remain unresolved. No release/merge/deploy/production DDL was performed.


## Phase 3 P0 transaction review continuation — exact-head draft #103 (2026-10-29 ET)

**Latest checked inventory:** 21 accessible repositories, **32 open issues**, **114 open PRs**: 90 Car Dealership, 21 Project1, 2 IT Readiness Toolkit and 1 profile. The other issue/PR totals in this document are timestamped historical snapshots.

**P0 #89 narrow implementation validated:** [Draft PR #103](https://github.com/danwiz/project0-cardealership/pull/103), stacked on CI-verified #102, compares the reviewer's persisted `session_revision` under the same JDBC `SELECT ... FOR UPDATE` account row lock already checking role and encoded credentials. It guards a deterministic ABA race: reviewer demoted then restored *after* Java verified-session check but *before* SQL lock would otherwise match the original role/hash. Adds a negative regression asserting denied approval and no purchase mutation.

**Evidence:** immutable commit `d56d9ec76fb12432bab3bc2b875302874f2ee373`, [Maven CI run #40983209417](https://github.com/danwiz/project0-cardealership/actions/runs/40983209417), **COMPLETED SUCCESS** on Java 11 and Java 17 with **328 tests/job, zero failures/errors/skips**, package `BUILD SUCCESS`. Both logs show `JdbcReviewerRevocationRaceTest` executed and passing, plus `PostgresqlSessionRevisionMigrationTest` executed on disposable PostgreSQL 16. [Issue #89 source and exact-SHA record](https://github.com/danwiz/project0-cardealership/issues/89#issuecomment-6512322181).

**Release decision remains NO-GO:** narrow test coverage is not equivalent to live transaction-process isolation, real lost-COMMIT/failover reconciliation, owner-grant review, full 90-PR dependency integration or independent security approval. Project1 vulnerability verdict still absent. Do not merge, deploy, publish or provision production resources.


## Phase 4 actual COMMIT acknowledgment transport fault — 2026-10-29 ET

**Most recent verified working set:** 21 accessible repositories, **32 open issues**, **115 open pull requests**: 91 Dealership, 21 Project1, 2 Toolkit, 1 profile. Earlier snapshots remain historical.

**Verified new draft [#104](https://github.com/danwiz/project0-cardealership/pull/104)**, stacked on #103, exact commit `490f935049005dfe5c7e2871d92ec02c4ba3a5e5`. [Maven CI run #40984776835](https://github.com/danwiz/project0-cardealership/actions/runs/40984776835) **completed SUCCESS**. Java 11 and Java 17 each passed **329 tests, zero failures/errors/skips**, including `PostgresqlCommitAckTransportLossTest` executed (not skipped) and both test and package verification BUILD SUCCESS.

Unlike the earlier injected 08006 exception, this CI-only test uses an **actual ephemeral TCP proxy** to relay PostgreSQL 16 connection bytes: it forwards COMMIT to the server, **observes backend idle ReadyForQuery**, drops the completion acknowledgment, and cuts the client connection. JDBC must report the outcome **uncertain without automatic replay**. Independent direct PostgreSQL readback confirms one ACCEPTED request, one stock decrement, exactly one ownership and one payment plan; a deliberate same-request replay *after independent readback* remains idempotent. PostgreSQL SSL is deliberately disabled **only** on the disposable fixture proxy, never proposed for production.

This **does not** validate PostgreSQL primary crash/failover, packet loss before COMMIT reaches the server, in-flight backend termination, standby/replica-lag reconciliation, or integration of the separately permissioned SQL permit/receipt function into an authenticated production runtime. These are explicit P0 **NO-GO** gates.

**New detailed evidence and acceptance matrix:** [POSTGRESQL-PURCHASE-FAILURE-MODE-ACCEPTANCE-MATRIX-2026-10-29.md](POSTGRESQL-PURCHASE-FAILURE-MODE-ACCEPTANCE-MATRIX-2026-10-29.md). [#89 exact-head evidence](https://github.com/danwiz/project0-cardealership/issues/89#issuecomment-6512539039) and [#85 dependency tracker](https://github.com/danwiz/project0-cardealership/issues/85#issuecomment-6512539914).

No production DDL, service provisioning, deployment, main/master merge, release publication, or historical artifact rewrite. Draft PR #104 remains open and unmerged.


## Phase 5 TX-05 real pre-COMMIT transport failure — October 29, 2026 ET

**No new PRs:** extended the existing, still-draft/unmerged [Dealership PR #104](https://github.com/danwiz/project0-cardealership/pull/104). **Current confirmed totals:** 21 accessible repositories; 32 open issues; **115 open PRs** (91 Dealership, 21 Project1, 2 Toolkit, 1 profile). Counts are checkpoint-specific.

**Exact head `45eccdc73ce36d4298326498a3603e2363251fd6`**, [GitHub Actions #40985413694](https://github.com/danwiz/project0-cardealership/actions/runs/40985413694) **completed SUCCESS**, Java 11 and 17 with **330 tests per job, zero failures/errors/skips**, full Maven package verification. Both job logs explicitly show `PostgresqlCommitAckTransportLossTest`: **two executed cases** (test and verify phases, per Java job), none skipped.

- **TX-04 after server COMMIT completion**: CI TCP proxy forwards actual COMMIT, sees server idle ReadyForQuery, drops the acknowledgment before the client receives it; client reports uncertain transaction, a separate PostgreSQL 16 connection confirms exactly one fully committed purchase.
- **TX-05 before PostgreSQL receives COMMIT**: proxy cuts both TCP sockets **without forwarding the outbound COMMIT command**; client reports unknown transport outcome, independent readback confirms request still PENDING, stock unchanged (2), zero ownership/payment plans and no implicit retry. This demonstrates rollback in the isolated no-competing-writer test; it does not run the separate SQL permit receipt API or independently prove a production `NOT_CONFIRMED` receipt.
- Both cases are disposable CI-only (strict environment guard, random schema, transient localhost relay, intentionally plaintext proxy for wire observation). No production TLS bypass or credentials.

**Remaining P0 NO-GO**: fault during in-flight backend COMMIT, PostgreSQL primary crash/standby promotion and replica lag, production issuer/writer/reconciler authentication and isolated permissions, payment ledger/audit validation, cross-branch #85 reconciliation and independent DBA/SRE/security review. [Updated failure-mode acceptance matrix](POSTGRESQL-PURCHASE-FAILURE-MODE-ACCEPTANCE-MATRIX-2026-10-29.md); [issue #89 evidence](https://github.com/danwiz/project0-cardealership/issues/89#issuecomment-6512619677).

No default-branch merges, production SQL/secret changes, external provisioning, deployments or releases. The audit PR itself remains draft.


## Phase 6 consolidation — 91 PR graph, proposed canonical ADR and PBKDF2 parity (2026-10-29 ET)

**Latest exact inventory remains 21 accessible repositories, 32 open issues and 115 open PRs**, of which **91 are open draft Car Dealership PRs**. Live REST metadata verified two common roots (#5/#6), 84 long-stack, four short-stack and one independent documentation PR (#46). Latest long #104 SHA `45eccdc73ce36d4298326498a3603e2363251fd6`; short #84 SHA `086fbf91294f74fe4bd967256498ef94e92c501a`. Long is 341 exclusive commits ahead and 109 behind short; relative to `master` it is 356 ahead/16 behind. These are exclusive commit counts, not conflict/PR counts. The 16 shared changed paths, 9 short-only and 9 `master`-side changed paths are now enumerated with decisions in the [updated source-level register](CAR-DEALERSHIP-INTEGRATION-DECISION-REGISTER-2026-10-29.md).

**Canonical source/provenance still requires approval.** [Proposed ADR](ADR-CAR-DEALERSHIP-CANONICAL-REPOSITORY-2026-10-29.md) records that the separate `Project0-Cardealership-Maven` README explicitly names that repository the authoritative modernization target, whereas all 91 active draft PRs live in `project0-cardealership`. No code moved between repositories.

**New concrete P0 pre-merge security blocker:** `master` `Pbkdf2PasswordHasher` uses PBKDF2-HMAC-SHA256 600k iterations with 2m verify cap, 512-character encoded limit, fixed 16-byte salt/256-bit key checks; long #104 creates 120k hashes and accepts unbounded stored iteration/key-length inputs. Direct source/negative-test comparison confirms master-only hardening could be dropped by wholesale promotion. See [issue #29](https://github.com/danwiz/project0-cardealership/issues/29#issuecomment-6512754077) and [legacy hash migration plan](PBKDF2-INTEGRATION-AND-LEGACY-CREDENTIAL-MIGRATION-PLAN-2026-10-29.md).

An **isolated parity prototype** `security/integration-candidate-master-pbkdf2-parity-20261029` was created from immutable long #104 head; only `Pbkdf2PasswordHasher.java` and `Pbkdf2PasswordHasherTest.java` were copied from master with matching blob hashes. Candidate SHA `2ebcebb62b7668f5e9c89393726e183c4eb8abe2`, [CI #40986769490](https://github.com/danwiz/project0-cardealership/actions/runs/40986769490) was **in progress** when noted. It is **NOT** a completed merge of short or `master`; do not imply production compatibility for existing 120k account hashes without a separate bounded rehash-on-login/forced rotation migration.

**No additional PR was opened or merged for the parity branch**. #85 remains P0 open, canonical repository pending owner decision, independent review outstanding and release NO-GO.


## Phase 7 — PBKDF2 parity and opt-in historical credential upgrade verified (2026-10-29 ET)

**Exact isolated integration branch** `security/integration-candidate-master-pbkdf2-parity-20261029` at commit `eadc05748a1c0481d16bf97f3edeebc086170d94`: [Maven CI run #40987971029](https://github.com/danwiz/project0-cardealership/actions/runs/40987971029) **COMPLETED SUCCESS**. Java **11 and 17 each passed 337 tests, zero failures/errors/skips**, including `LegacyPbkdf2CredentialUpgradeTest` (6 non-skipped), strong `Pbkdf2PasswordHasherTest` (4), and actual PostgreSQL COMMIT transport-loss tests (2); Maven package verification BUILD SUCCESS.

The parity candidate retains **exact `master`** PBKDF2 implementation and tests (600k default, capped 2m verifier and size/salt/key bounds). A separate `LegacyPbkdf2CredentialUpgrade` class enables **explicitly provisioned, disabled-by-default** migration of only the exact historical 120k encoded PBKDF2 format with bounded fixed-size parsing and constant-time comparison. `UserLoginService` now supports an optional trusted credential-writer capability; after verified legacy password, credential CAS stores a new 600k hash, rotates the account session revision and verifies the reloaded persisted identity before returning success. Unconfigured default login still denies weak hashes.

**Limitations:** The migration writer is **not wired into normal runtime**, existing user-account hashes were not inventoried or exported, and no production data or database was changed. Authenticated application-context session issuance, production-limited writer privileges, rate limiting, audit forwarding, rollback and independent signoff remain unverified. This is an **isolated prototype branch**, not a merged canonical integrated product; #85, #89, #29 and Project1 P0 gates remain **NO-GO**. [Detailed migration policy and exact-head acceptance](PBKDF2-INTEGRATION-AND-LEGACY-CREDENTIAL-MIGRATION-PLAN-2026-10-29.md); [issue #85 evidence](https://github.com/danwiz/project0-cardealership/issues/85#issuecomment-6513005941).

**Open PR count remains 115**, because this prototype did not create a pull request. No default-branch merges, releases, production schema migrations or external provisioning.


## Phase 8 — authenticated legacy credential session and short-branch parity — 2026-10-29 ET

**Strong credential migration through the actual application boundary is CI-verified.** [Maven Actions #40991023039](https://github.com/danwiz/project0-cardealership/actions/runs/40991023039), exact isolated candidate commit `768e9998b7ea9477ebfa8a8fe22d2699a98b3c91`, **COMPLETED SUCCESS**, Java 11 and Java 17 each passed **339 tests, 0 failures/errors/skips**; both job logs show **2 non-skipped `LegacyCredentialApplicationSessionIntegrationTest`** tests in the test and verify/package phases. In-memory and JDBC/H2 synthetic historical accounts were upgraded by a **separately supplied opt-in writer**, then successfully logged in through the unchanged `AuthenticateAccountCommand`, `ContextIdentityAdapter` and verified `RoleAuthorizationService`. Forged admin identity was denied, customer privileges remained limited, and a later credential rotation revoked the session. The normal runtime remains strict and does not install legacy migration.

**Short-branch behavioral parity** is now enumerated in a dedicated [22-case disposition matrix](CAR-DEALERSHIP-SHORT-BRANCH-BEHAVIORAL-PARITY-2026-10-29.md): six role/facade, five inventory and eleven purchase review tests from short #84. Most are mapped to current typed/JDBC security invariants; **I-02/I-03/I-04** were partial for actual authenticated customer/forged actor/deleted employee inventory commands. Added two targeted tests to the isolated integration candidate, commit `e4a24a588c8faa92cabb6f4ec0c7ca1b463550a3`, covering both memory and JDBC/H2. [Java 11/17 CI #40991436945](https://github.com/danwiz/project0-cardealership/actions/runs/40991436945) was **in progress** at this checkpoint. Never mark it passing until both exact-head job logs confirm the two tests and package verification.

**Pending purchase parity gaps:** P-02 revoked reviewer in actual command, P-03 authenticated pending-buyer projection, P-04 orphan/missing buyer handling (note PostgreSQL schema FK prohibits orphan requests at creation), P-08 preservation of pre-existing ownership under rollback, P-11 invalid payment-term behavior. Do not transplant the competing best-effort in-memory rollback implementation into the JDBC ACID writer.

**Counts unchanged** from prior verified inventory: 21 accessible repositories; 32 open issues; 115 open PRs. This phase added test files and documentation only on existing isolated branch/draft portfolio PR, **not new PRs or default branch merges**. #85 canonical repository and production release remain NO-GO.

## Phase 8 exact-head test verification — short inventory parity (2026-10-29 ET)

**Final result supersedes the earlier in-progress note:** isolated candidate `security/integration-candidate-master-pbkdf2-parity-20261029`, commit `e4a24a588c8faa92cabb6f4ec0c7ca1b463550a3`, [Maven CI #40991436945](https://github.com/danwiz/project0-cardealership/actions/runs/40991436945) **COMPLETED SUCCESS**, **341 tests each on Java 11 and Java 17**, 0 failures/errors/skips, BUILD SUCCESS for test and package verify. Both job logs explicitly confirm four `SessionDemotionInventoryRegressionTest` executions and two `LegacyCredentialApplicationSessionIntegrationTest` executions, none skipped.

New direct command regressions transfer short branch I-02/I-03/I-04 by behavior: signed-in customer denied inventory mutation; copied admin/role/encoded-hash/session revision denied; wrong password rejected; deleted employee session denied without inventory change, in both memory and JDBC/H2 modes. [Behavioral parity register](CAR-DEALERSHIP-SHORT-BRANCH-BEHAVIORAL-PARITY-2026-10-29.md) updated to mark those test gaps **CI verified on isolated candidate**, not accepted for release.

**Outstanding**: short purchase-test parity P-02/P-03/P-04/P-08/P-11; exact final integrated SHA with master/short branch conflict resolution; canonical repository ADR; authenticated SQL issuer/writer/reconciler; PostgreSQL failover; Project1 vulnerability verdict; owner/DBA/security signoff. These remain P0 NO-GO. No new PR, no main/master merge, no production DDL, deployment, credential migration or release.


## Phase 9 — five remaining short-branch purchase-review parity tests (2026-10-29 ET)

Continuing from the exact-head **341-test** Java 11/17 CI success on `e4a24a588c8faa92cabb6f4ec0c7ca1b463550a3`, five targeted **test-only** regressions were added to the **same isolated integration branch** at `6b332471f8deb6e7308a18c9960c00141b860bf2`:

- `JdbcPurchaseBehaviorParityTest.revokedReviewerCannotApproveOrInspectPendingBuyers`: deleted reviewer denied; no writes.
- `pendingBuyerProjectionRequiresVerifiedReviewerAndPreservesRequester`: persisted buyer projection, protected immutable staff view.
- `missingBuyerIsRejectedAtForeignKeyBeforeCreatingAnOrphanRequest`: modern JDBC foreign key blocks invalid request at insertion; original late-approval orphan test is **not** directly applicable.
- `rolledBackSecondPurchasePreservesPreviouslyCommittedCustomerOwnership`: prior ownership/payment plan survives an injected new-purchase failure after tentative ownership write, with request/stock rollback.
- `authorizedReviewerCannotCreatePurchasesWithInvalidTerms`: direct and configured command rejects invalid months and negative request identifier with no writes.

**CI pending:** [Maven GitHub Actions #40995418505](https://github.com/danwiz/project0-cardealership/actions/runs/40995418505) testing this exact commit on Java 11 and 17. Do not mark these five cases completed until non-skipped test lines and both job conclusions are verified. [22-case behavioral parity crosswalk](CAR-DEALERSHIP-SHORT-BRANCH-BEHAVIORAL-PARITY-2026-10-29.md) and [issue #85](https://github.com/danwiz/project0-cardealership/issues/85#issuecomment-6513964265) updated.

**Release and integration still NO-GO:** no provenance or canonical Maven repo owner approval, no final resolved master/short integrated candidate, no PostgreSQL failover and production issuer/reconciler or independent security/DBA acceptance. No default-branch merge, new PR, production database, cloud credential, deployment or release.

## Phase 9 exact-head purchase parity CI acceptance — 2026-10-29 ET

**Previous five-case pending status superseded.** Isolated integration candidate `6b332471f8deb6e7308a18c9960c00141b860bf2` passed [GitHub Actions Maven CI #40995418505](https://github.com/danwiz/project0-cardealership/actions/runs/40995418505) **COMPLETED SUCCESS**. Both Java 11 and 17 job logs confirm **346 total tests each**, 0 fail/error/skip, including **five `JdbcPurchaseBehaviorParityTest` cases** executed and passing in test and verify phases.

P-02/P-03/P-04/P-08/P-11 are now covered on the **isolated JDBC/H2 candidate**, complementing the previous I-02/I-03/I-04 inventory parity and verified credential-session integration. The modern schema's FK rejects nonexistent buyer requests at insertion rather than allowing legacy orphan requests. This is a stronger transactional boundary, not evidence of identical original legacy behavior.

[22-case short-branch behavioral parity register](CAR-DEALERSHIP-SHORT-BRANCH-BEHAVIORAL-PARITY-2026-10-29.md) updated. The five-case proof does **not** merge the competing branches or establish PostgreSQL failover and production-authenticated receipt writer/reconciler. Issue #85 P0, #89, Project1 vulnerability scanning, canonical-repo ADR, independent review and complete integrated-release SHA are still **NO-GO**. Open PR count remains **115** because no new PR was opened.

## Phase 10 — master baseline provenance + workflow parity (2026-10-29 ET)

The **protected `project0-cardealership/master`** was independently pinned at immutable commit `90741d3abe51d9cc002aaeb1dacae27b933fba10`. A new [master-baseline preservation manifest](CAR-DEALERSHIP-MASTER-BASELINE-PRESERVATION-MANIFEST-2026-10-29.md) records exact Git blob SHA for the nine `master`-side changed paths, the six original historical characterization suites, the preserved security-hashing files and the modern behavioral dispositions. It distinguishes intentional historical defects from regressions: tests documenting double .dat appends/null dereference, pending list/index failure, overpayment and capacity limits, and unrestricted deletion are **preserved only as evidence**, not restored as modern expected behavior.

**Security parity proven at the source level:** `Pbkdf2PasswordHasher.java` and `Pbkdf2PasswordHasherTest.java` have identical Git blob hashes on protected `master` and the isolated modern candidate. The 600k default KDF work factor and bound-check regressions are preserved.

**CI workflow gap remediated only on the isolated candidate:** [commit `0cbad314956ad1d36542d30afa6519a1bbfecdce`](https://github.com/danwiz/project0-cardealership/commit/0cbad314956ad1d36542d30afa6519a1bbfecdce) restored the default `master` `push` branch trigger, retained `pull_request` on master, and ported the separate `diagnostics` job using `actions/download-artifact@v6`, while retaining Java 11/17 and isolated PostgreSQL16 jobs. [Exact-head Actions #40997446982](https://github.com/danwiz/project0-cardealership/actions/runs/40997446982) was **in progress when logged**. The 346-test success at preceding SHA `6b332471f8deb6e7308a18c9960c00141b860bf2` does **not** validate the new workflow or diagnostics job; check all four job conclusions and logs.

**NO-GO still applies**: no protected branch push/merge, full short/master code merge, Maven product import, production issuer/writer/reconciler, PostgreSQL failover, Project1 vulnerability verdict, independent review or release approval. The manifest records Git history and blob integrity but is not an offline archival Git bundle.
