# GitHub portfolio remediation plan — baseline 2026-10-29

**Scope:** 18 repositories; 22 currently open issues in 6 repositories. This is a discovery/control baseline, **not** a declaration of comprehensive source, workflow, or security verification. Do not merge, deploy, archive, or delete historical repositories on the strength of this plan.

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
