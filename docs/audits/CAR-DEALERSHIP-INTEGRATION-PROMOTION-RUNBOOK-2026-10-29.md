# Car Dealership — Canonical Integration, Promotion & Rollback Runbook

**Version:** 1.0 review draft · **Prepared:** 2026-10-29 ET  
**System:** `danwiz/project0-cardealership` → optional `danwiz/Project0-Cardealership-Maven` portfolio product  
**Record:** [issue #85](https://github.com/danwiz/project0-cardealership/issues/85) / [issue #89](https://github.com/danwiz/project0-cardealership/issues/89) / [audit PR #25](https://github.com/danwiz/danwiz/pull/25)  
**Current release state:** **P0 NO-GO**. This document specifies **future steps**, not permission to merge, tag, publish, provision or migrate production data.

## 0. Scope, governance and source-of-truth rule

- **Preserve** the historical Eclipse/training source and full commit graph; never rewrite, squash away or force-push original master or draft review branches.
- **Develop** one candidate: `security/integration-candidate-master-pbkdf2-parity-20261029` (current SHA below). This is a **technical test candidate**, not yet a branch incorporating every competing Git parent.
- **Choose** a canonical portfolio destination **before cross-repository movement**. [ADR](ADR-CAR-DEALERSHIP-CANONICAL-REPOSITORY-2026-10-29.md) provisionally prefers the Maven repo because its README explicitly declares it authoritative. The owner has **not signed** the decision.
- **Promote once** only when exact-SHA tests, provenance, security, disaster recovery and operating roles pass independent review. Do not confuse a green *nested development PR* with final release approval.
- **Do not merge 91 draft PRs one by one** or automatically close them. Each dependency/branch has preserved, superseded, redundant or accepted-by-equivalence disposition and evidence. No history rewrite.

## 1. Immutable checkpoints — re-read before executing

| Ref / authority | Exact GitHub-observed SHA | State |
| --- | --- | --- |
| Historical protected `project0-cardealership/master` | `90741d3abe51d9cc002aaeb1dacae27b933fba10` | Source baseline, immutable preservation |
| Shared long/short ancestor | `ad8d03574c7f048b236c9d24f0c03ac54dffcbd7` | Genealogical reference |
| Long/master merge ancestor | `9c242f9880a18a7749621a6ed5f6d53d3ee5fcdc` | Genealogical reference |
| Last unmerged long PR #104 | `45eccdc73ce36d4298326498a3603e2363251fd6` | Draft, nested on #103 |
| Last unmerged short PR #84 | `086fbf91294f74fe4bd967256498ef94e92c501a` | Draft, nested on #83 |
| Isolated integrated **test** candidate | `0cbad314956ad1d36542d30afa6519a1bbfecdce` | Java 11/17 + PG16 CI proof only |
| Separate Maven repository `master` | `a8dce295b9ab45ca6e896035bb81788bd4aff217` | Proposed but **unapproved** canonical portfolio destination |
| Independent docs/cleanup PR #46 | `235dd4c29d0f9b88e96fa3790675f0ad67a16949` | Unmerged draft against historical master |

**Observed PR topology:** 91 open **draft** dealership PRs = two common roots (#5/#6), 84 long-chain PRs, four short-chain PRs (#78/#82/#83/#84), one independent docs PR #46. Candidate vs short: **350 commits ahead/109 behind**. Candidate vs historical master: **365 ahead/16 behind**. These are exclusive Git commit counts, **not** the number of merge conflicts or proof of missing functionality.

The latest candidate [Actions #40997446982](https://github.com/danwiz/project0-cardealership/actions/runs/40997446982) completed **SUCCESS**: Java 11 and Java 17 each **346 tests, 0 failure/error/skip**, with **both independent Maven diagnostics jobs passing** and downloading/printing Maven log artifacts. This proves the isolated candidate at the above SHA, **not** any subsequent integration, destination import or production service.

**Freshness gate:** fetch all refs again immediately before staging; if any differ, stop, update this source register, and re-run comparisons. Never use a branch label alone as a proof of the accepted tree.

## 2. Canonical repository and engineering policy decision (G0)

**Owner must approve exactly one:**
- **Option A (provisionally preferred):** `project0-cardealership` = historical record + integration work; `Project0-Cardealership-Maven` = eventual portfolio product. Candidate code is ported to a dedicated **destination review branch** only after complete integration and tests. Preserve immutable origin SHA, authors, third-party license evidence and import manifest.
- **Option B:** modernize `project0-cardealership` directly, preserve original history and separately classify/retire the Maven duplicate. Destination `master` must receive the signed-off integrated tree through protected PR.
- **Option C:** two active applications only with two different approved product requirements, maintainers and independent CI/security ownership; otherwise **reject** due to duplicated vulnerable surfaces.

**Required decision metadata:** accountable owner, approved ADR SHA, product name and intended customers, portfolio-only vs production intent, Java support matrix, serialization-to-JDBC migration scope, author/license attribution, README and domain redirects, version numbering and rollback authority. No default branch changes before decision.

## 3. Preservation and evidence freeze (G1)

1. Record immutable Git source commit SHAs, parent graph, **all relevant Git blob hashes**, candidate workflow digest, original tests, binary artifacts, README and license notices. See [master manifest](CAR-DEALERSHIP-MASTER-BASELINE-PRESERVATION-MANIFEST-2026-10-29.md), [16-overlap/9-short/9-master disposition register](CAR-DEALERSHIP-INTEGRATION-DECISION-REGISTER-2026-10-29.md), and [22-case parity register](CAR-DEALERSHIP-SHORT-BRANCH-BEHAVIORAL-PARITY-2026-10-29.md).
2. Make an independently stored read-only **Git bundle/clone mirror** (not performed by this chat); verify refs and `git fsck`, record SHA-256 checksum, custody, timestamp, approver and restore instructions. GitHub history alone is not an offline backup.
3. Inventory `bin/`, `target/`, `.classpath`, `.project`, `.settings/`, compiled `.class`, `.dat`, fixtures and generated files **without deleting historical objects**. PR #46 proposes cleanup of 12 tracked `.class` and Eclipse metadata files; review independently. Separate the future distribution tree's tracked files from historical provenance.
4. Confirm third-party attribution, original academic code ownership, SPDX license decision, dependency license/SBOM; neither repository root currently showed a top-level LICENSE in the inspected trees. **Do not invent a license** or assume public visibility grants redistribution rights.
5. Record user-account credential **version cohorts without dumping hashes or real user identifiers**; no real data was inspected in CI. A private, access-controlled source-data inventory and verified backup are mandatory before any migration.
6. Stop if the provenance inventory cannot be reconciled or any potential secret/private data is found in a proposed public distribution. Quarantine with authorized security review before publishing.

## 4. Read-only ancestry and conflict drill (G2)

**A. Refresh and inspect — proposed commands, NOT executed here:**

```bash
git clone https://github.com/danwiz/project0-cardealership.git dealership-reconciliation
cd dealership-reconciliation
git fetch --prune origin
git rev-parse origin/master
git rev-parse origin/security/integration-candidate-master-pbkdf2-parity-20261029
git rev-parse origin/fix/atomic-account-create-20261029
git merge-base origin/master origin/security/integration-candidate-master-pbkdf2-parity-20261029
git log --left-right --cherry-pick --oneline origin/master...origin/security/integration-candidate-master-pbkdf2-parity-20261029
git diff --name-status origin/master...origin/security/integration-candidate-master-pbkdf2-parity-20261029
git diff --name-status origin/fix/atomic-account-create-20261029...origin/security/integration-candidate-master-pbkdf2-parity-20261029
git fsck --no-reflogs
```

**B. Dry-run without writing the default branch.** A local `git merge-tree --write-tree` reports a merge result/tree or conflicts without changing working tree or remote refs; capture stdout/stderr and return code rather than assuming clean compatibility. If conflicts are found, enumerate all files and both proposed resolutions in an approved decision record. Do not use `-X ours` or `-X theirs` globally:

```bash
git merge-tree --write-tree origin/master origin/security/integration-candidate-master-pbkdf2-parity-20261029
```

**C. Only after G0/G1 and reviewer authorization:** create a local disposable **source integration branch based on the protected master snapshot** (not a direct merge into master):

```bash
git switch -c integration/reconcile-source-YYYYMMDD origin/master
git merge --no-commit --no-ff origin/security/integration-candidate-master-pbkdf2-parity-20261029
# Review conflict inventory, staged tree, and master-specific security+historical fixtures.
# DO NOT commit or push unresolved changes. Abort at any sign of unapproved loss.
git diff --check
git status --short
# To abandon the uncommitted integration:
git merge --abort
```

Do not blindly replay the short branch's best-effort in-memory purchase compensation. Treat its four-PR path as **behaviorally reconciled** only to the extent the [22-case parity suite](CAR-DEALERSHIP-SHORT-BRANCH-BEHAVIORAL-PARITY-2026-10-29.md) maps tests: all five late purchase gaps were tested in JDBC/H2 at candidate SHA `6b332471f8deb6e7308a18c9960c00141b860bf2`; a final candidate needs those passing again. Explicitly adjudicate any additional short-only docs, ports, historical test semantics and third-party rights.

## 5. Required source resolution order (G3)

| Order | Change set | Treatment | Proof |
| --- | --- | --- | --- |
| 1 | Protected `master` PBKDF2 source/tests | Preserve **exact 600k default**, max-2m verification bound, bounded representation, fixed salt/key; do not revert to the long branch's 120k new-hash default | Blob SHA parity, hostile input tests, Java11/17 |
| 2 | Modern account/session authorization | Retain verified actor binding, persisted `session_revision` revocation, CAS credential change; migrate historical 120k only through explicitly authorized, **disabled-by-default** upgrade | In-memory, JDBC/H2, PG16 schema and real app-session reauthentication |
| 3 | JDBC purchase integrity | Retain SERIALIZABLE stock/request/ownership/payment plan transaction and reviewer row-lock revision check; no auto replay when COMMIT outcome unknown | PG16 TX-01–TX-05 and permit/receipt checks; TX-06/07/11 still NO-GO |
| 4 | Short branch customer, inventory, purchase tests | Port **behavioral parity**, not duplicate competing service layers or unsafe compensation | 22-case matrix, 346-test candidate suite, diff-to-test mapping |
| 5 | Six historical `master` characterization suites | Preserve exact historical source and Git blobs, retain modern corrected expectation in current suite | Source manifest and reviewer evidence that bugs were intentionally fixed |
| 6 | `master` CI semantics | Retain `master` push CI, PR protection, read-only contents, Java11/17+PG16, separate Maven diagnostics | Four-job [#40997446982](https://github.com/danwiz/project0-cardealership/actions/runs/40997446982) on candidate; **repeat on final SHA** |
| 7 | Independent PR #46 README/artifact hygiene | Adapt useful docs and future clean-tree policy without removing historical files or silently overwriting modern docs | Files/hashes, CI, provenance, link/README review |
| 8 | Remaining master-exclusive commits and short-only paths | Owner-signed explicit dispositions; no silent `ours`/mass close | Final file manifest; reviewable merge commit parents and Git diff |

**Acceptance:** every source-side conflict has a decision ID; every preservation item has a stable content hash and source URL; tests show no weakened security, lost history, or duplicate domain writer.

## 6. Destination compatibility and package promotion (G4)

The candidate source repo and the proposed Maven destination are **not interchangeable builds**:

| Contract | Source integration candidate | Existing Maven destination |
| --- | --- | --- |
| Java | Maven compiler `release=11`; CI on Java 11 & 17 | Compiler `release=17`; CI Java 17 |
| Source tree | Legacy Eclipse `src/com/revature/...` with explicit Maven `sourceDirectory=src` | Standard `src/main/java` and `src/test/java` |
| Tests | **JUnit Jupiter 5.11.4**; PG16/H2 | **JUnit 4.13.2** |
| Persistence | JDBC/H2/PostgreSQL16 + guarded legacy snapshots | Legacy local Java serialization |
| Dependencies | H2 2.3.232, PostgreSQL JDBC 42.7.14 | Log4j 2.26.1, no JDBC driver |
| Maven coordinates | `com.revature:project0-cardealership:1.0.0-SNAPSHOT` | `com.revature:cardealer:0.1.0-SNAPSHOT` |
| Tracked generated files | Historical source repo includes `bin/` | Maven repository includes **tracked `target/` files** |
| Root licensing | No top-level LICENSE shown in inspected root | No top-level LICENSE in complete tree scan |

**Do not `cp -r` all files into destination master.** If Option A is approved: stage a new **non-default** review branch in the Maven repository, create a `src/main/java`/resources and test tree mapping, consciously migrate POM coordinates, Java policy and JUnit5 dependencies, inventory Log4j use before removal, retain only approved supported adapters, package fixtures offline, and remove generated target files **only from the new distribution tree** with a preservation manifest. A final CLI smoke test must be runnable from clean checkout.

The destination's `master` currently is `a8dce295b9ab45ca6e896035bb81788bd4aff217`. Require explicit security/owner acceptance of any cross-repo code transfer and license provenance before branch creation or public pushes.

## 7. Final release candidate verification (G5)

**The full release-candidate SHA must change after source/destination integration, then all evidence is invalid until retested on the new SHA.**

Minimum independent checks:
1. Reproducible **clean-room** checkout, Maven `clean verify` on approved JDK matrix, no local IDE files or generated binaries; compare built artifacts and dependency provenance where supported.
2. Unit, console/CLI, authenticated account and role mutation, historical migration and revocation, short-branch **22-case behavioral parity**, network isolation, snapshot file safety, immutable queries and purchase/payment projections.
3. PostgreSQL16 **real** schema/owner/writer/reader grants, definer function `search_path`, default role DDL denial, trigger rotation, serializable concurrency, actual pre-COMMIT and post-COMMIT-ack network loss, reconciliation status and durable receipts. **TX-06 in-flight COMMIT, TX-07 failover/WAL, TX-11 stale replica remain explicit physical fault gates**.
4. Per-environment credential source and minimum privileges (issuer, writer, reconciler each independent, no shared CI owner credential outside CI); TLS, credential rotation, append-only auditable receipts, signed evidence verification and incident runbooks.
5. Static dependency and secret scanning; dependency review and **SBOM**, license attribution, automated CI permissions/third-party action version review, no archived private secrets in README/build/release.
6. Full final PR review (owner, independent security/DBA, QA/SRE) including **artifact hashes, signed provenance, restore rehearsal and rollback owner**. Require written resolution of P0 #85/#89/#98/#99 and Project1's vulnerability verdict; do not declare unrelated repo issues closed merely because this project passes.
7. README badges, architecture, threat model, install/test/CLI examples, support matrix, expected limitations, historical origin and cross-repo links; Pages/pinned portfolio only after owner signoff and publish approval.

**Pass criterion:** CI jobs on the exact *final* integrated SHA complete SUCCESS, all required named tests actually executed (no unapproved skips), review approvals signed and evidence logged. Do not use test count alone as an acceptance proxy.

## 8. Deployment and rollback (G6) — future procedures, NOT executed

| Stage / fault | Safe response | Irreversibility consideration |
| --- | --- | --- |
| Before integration commit | `git merge --abort` on the disposable local branch; keep original refs | No shared history changed |
| After branch commit, before any protected PR merge | Close or supersede disposable PR **only after audit**; retain branch, logs, SHAs and bundle | Never force-push history; docs can point to rejected candidate |
| After approved protected merge, no production rollout | Use reviewed inverse commit via normal protected PR; e.g. `git revert -m 1 <merge-commit>` **only after identifying first-parent role and verifying reversal with tests** | Revert of shared integration may conflict; do not delete merge history |
| Application rollout with no schema change | Roll back application binary to last approved image/artifact digest **only if** stored data and security semantics remain backward-compatible | Older binaries might accept weak hashes or stale sessions; never silently reactivate revoked sessions |
| PostgreSQL schema or credential migration | Stop new writes, preserve WAL/audit/receipt evidence, use DBA-approved restore-forward or compatible rollback plan and independently reconciled receipts | Credential CAS/session revisions, new ownership and receipt writes are **not** safely reversible by an unreviewed DB restore |
| Uncertain COMMIT after network failure | Do not automatically retry approval. Reconcile original request/contract via independently authorized, primary-consistent read-only receipt; `UNKNOWN` or `INCONSISTENT` blocks writes | `NOT_CONFIRMED` at one instant is **not** proof no in-flight transaction can commit |
| Failover/replica lag | Block further approval and promotion; keep original correlation IDs and receipts; require DBA/SRE primary-consistency proof and reconciliation before reopen | RPO/RTO **unknown** until tested; do not promise zero loss |
| Secret, audit or license incident | Halt deployment, preserve evidence and notify authorized owners; perform appropriate credential rotation/access revocation, not a public incident dump | Avoid revealing active tokens or credential hashes |

**Rollback success criteria:** previously accepted purchases remain singular, stock cannot be double-decremented, payment-ledger consistency is audited, verified sessions remain safely revoked, migration cannot downgrade PBKDF2, immutable evidence survives, and fresh exact-head CI/security checks pass.

## 9. Stage model and stop/go decision record

| Stage | Current state | Exit gate |
| --- | --- | --- |
| Historical source | **Preserved / archived evidence** | Signed provenance and independent off-GitHub backup |
| Security modernization | **Development + CI-tested prototype** | Approved source merge and all P0 security controls |
| Integration | **Source/behavior reconciled in documents and one test branch; ancestry NOT merged** | Explicit conflict resolution; exact final SHA, clean-run full tests |
| Staging | **Not established** | Restricted PostgreSQL environment, infrastructure policy, backup/restore/failover rehearsal |
| Production | **Not authorized** | Owner/DBA/security/SRE approvals, clear rollback, release gates |
| Portfolio publication | **Not approved** | Canonical repo owner decision, complete README/attribution, security scan and signed tag |

### Required approval record (complete before proceeding)

```text
ADR option approved (A/B/C):              PENDING
Owner + timestamp + immutable ADR SHA:     PENDING
Historical source backup location/hash:   NOT CREATED/VERIFIED
Approved final source integration SHA:     NONE
Approved Maven destination SHA (if A):    NONE
Conflicts closed and disposition signoffs: PENDING
License/attribution review:               PENDING
PostgreSQL SQL roles / issuer & receipt:   PENDING
Failover and stale-read rehearsal:         PENDING
Project1 vulnerability verdict:           PENDING
Independent QA/security/DBA signoff:       PENDING
Artifact digest and rollback rehearsal:   PENDING
Release tag and publisher approval:       NOT AUTHORIZED
Decision:                                 **NO-GO**
```

**No commands in this runbook were executed against production or protected branches by publishing this document.** Open draft PRs, original artifacts, source `master` and Maven destination `master` remain untouched.

## 10. Phase 12: real Git-object preflight — screened, not merged (2026-10-29 ET)

**New verified evidence:** [Five immutable Git trees + machine-readable three-way blob collisions](CAR-DEALERSHIP-THREE-WAY-BLOB-COLLISION-INVENTORY-2026-10-29.json) and [22-path reviewer triage](CAR-DEALERSHIP-THREE-WAY-COLLISION-TRIAGE-2026-10-29.md). The GitHub API returned `truncated=false` for all five recursive trees. Against common ancestors, **master/candidate has seven differently modified paths and two identically changed paths** (both PBKDF2 files); **short/candidate has 15 different two-sided paths (13 modify/modify, two add/add) and one identical** (PaymentPlanTest). The candidate's `OwnedVehicle` adds durable ownership and contract IDs; `PaymentPlan` is behaviorally comparable but adds serialization support. Preserve the current candidate's stronger model, pending owner review.

**Hard limitation:** A local `git ls-remote` attempt from this environment failed with DNS resolution for github.com. **No actual Git merge-tree was run** and **no full off-GitHub Git bundle was generated or restored**, so G01 and G02 remain open. A [syntax-checked shell helper](tools/rehearse-dealership-source-merge.sh) is committed to this draft audit to do the full mirror, SHA-fenced bundle, checksum/fsck and two local merge-tree drills when executed in a Git-network-enabled environment. It refuses nonempty output and never pushes to remote; its end-to-end live behavior has **not** been tested here.

**Do not interpret the blob overlap counts as Git merge conflict counts.** The reviewed dispositions and machine registry are planning/evidence, not an accepted merge tree. [Release-gate register](CAR-DEALERSHIP-RELEASE-GATE-REGISTER-2026-10-29.json) remains **17 gates, 12 blocking, release_authorized=false, NO-GO**.
