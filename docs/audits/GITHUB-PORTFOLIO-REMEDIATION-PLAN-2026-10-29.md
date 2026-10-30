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
