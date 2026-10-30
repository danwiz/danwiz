# Car Dealership — Three-Way Git Object Collision Triage

**Capture:** October 29, 2026 ET. **Status:** review screening, NOT a Git merge-tree run or release decision.
**Source:** `danwiz/project0-cardealership` GitHub Git Trees API (all five returned `truncated=false`).  
**Machine-readable exact blob evidence:** [JSON collision inventory](CAR-DEALERSHIP-THREE-WAY-BLOB-COLLISION-INVENTORY-2026-10-29.json).  
**Safe local executor:** [read-only remote archive and merge-tree rehearsal script](tools/rehearse-dealership-source-merge.sh).

## 1. What has actually been established

Immutable source heads:
- Protected `master` = `90741d3abe51d9cc002aaeb1dacae27b933fba10`.
- Isolated candidate = `0cbad314956ad1d36542d30afa6519a1bbfecdce`.
- Competing short #84 = `086fbf91294f74fe4bd967256498ef94e92c501a`.
- `master`/candidate common base = `9c242f9880a18a7749621a6ed5f6d53d3ee5fcdc`.
- Short/candidate common base = `ad8d03574c7f048b236c9d24f0c03ac54dffcbd7`.

| Comparison against common ancestor | Both sides have **different** final blobs | Both sides have **identical** changed blobs |
| --- | ---: | ---: |
| Protected `master` vs isolated candidate | **7** (all modify/modify) | **2** |
| Short #84 vs isolated candidate | **15** (13 modify/modify, **2 add/add**) | **1** |

**Important technical distinction:** these are precise Git object/blob differences from a common ancestor, **not actual textual merge conflicts**. A source file may have two different blobs yet merge automatically when edits do not overlap. An add/add collision with different content is particularly likely to require explicit resolution. The GitHub API exposes this file-level evidence but does not perform the local Git recursive/ort merge resolution.

## 2. Seven differently changed master paths — reviewer disposition

| Path relative to repository | Proposed disposition | Acceptance |
| --- | --- | --- |
| `.github/workflows/maven-ci.yml` | **Retain integrated CI version** | Protected `master` push coverage and independent diagnostics now restored on isolated candidate; Java11/17+PG16 four-job [CI #40997446982](https://github.com/danwiz/project0-cardealership/actions/runs/40997446982) passed; run again after actual merge |
| `src/test/java/com/revature/DAOService/DAOServiceCharacterizationTest.java` | **Retain modern corrected behavior** | Original appended `.dat`, null/missing result behavior remains SHA-pinned in master manifest |
| `src/test/java/com/revature/cardealer/CarDealershipCharacterizationTest.java` | **Retain corrected auth/console behavior** | Original downcast/null-dereference and reference-equality cases preserved as archival evidence |
| `src/test/java/com/revature/cardealer/OfferCharacterizationTest.java` | **Retain modern bounded/stable request behavior** | Historical index/pending-list failures captured in master manifest |
| `src/test/java/com/revature/cardealer/PaymentsCharacterizationTest.java` | **Retain corrected ledger assertions** | Historical negative balances and 20-entry boundary retained in original source |
| `src/test/java/com/revature/service/RoleLoginServiceCharacterizationTest.java` | **Retain modern authenticated ownership behavior** | Historical fixed-array and null-owner cases documented |
| `src/test/java/com/revature/service/UserLoginServiceCharacterizationTest.java` | **Retain fail-closed deletion** | Do not reactivate unprivileged account deletion to pass old tests |

The **two identical changed blobs** are `src/com/revature/service/Pbkdf2PasswordHasher.java` and `src/test/java/com/revature/service/Pbkdf2PasswordHasherTest.java`. Preserve these exact 600,000-iteration, bounded-validation master versions; secure lower-work-factor credential migration is separately opt-in.

These file choices are **proposals for a future merge resolution**, not completed merge resolutions. Original historical source remains accessible at the protected pinned master SHA and should be backed up independently before publication.

## 3. Fifteen distinct changed paths against the short stack

| Path | Risk class | Proposed integration policy |
| --- | --- | --- |
| `.github/workflows/maven-ci.yml` | CI trust and triggers | Preserve current 4-job PG16 and protected master trigger; compare short-only checks |
| `src/com/revature/cardealer/CarDealership.java` | Console actor authorization | Modern context-verified command dispatch; do not restore no-actor persistence |
| `src/com/revature/cardealer/Offer.java` | Purchase/request state | Retain stable listings and single-winner purchase transitions; preserve legacy behavior evidence |
| `src/com/revature/cardealer/OwnedVehicle.java` | **ADD/ADD** | Candidate adds `Serializable`, immutable ownership ID and optional normalized contract ID; short version is just vehicle/plan holder. **Prefer candidate**, subject to serialization and schema review |
| `src/com/revature/cardealer/PaymentPlan.java` | **ADD/ADD** | Both versions implement same positive-payment/no-overpay and term-validation semantics, but candidate implements `Serializable` with `serialVersionUID=1L`. **Prefer candidate**, test schema/snapshot compatibility |
| `src/com/revature/service/AdminLoginService.java` | Role permissions | Retain verified principal/admin bootstrap safeguards |
| `src/com/revature/service/CustomerLoginService.java` | Registration privilege | Preserve role-scoped self-registration; deny employee privilege |
| `src/com/revature/service/EmployeeLoginService.java` | Privileged operations | Preserve trusted operator path and revision revalidation |
| `src/com/revature/service/InMemoryUserAccountRepository.java` | Account concurrency/revision | Preserve candidate's insert-only creation, defensive copy, credential/role compare-and-swap and revision rotation |
| `src/com/revature/service/UserLoginService.java` | Identity/credential safety | Preserve bounded 600k PBKDF2 new hash policy, opt-in 120k migration, privileged mutations and no untrusted session escalation |
| `src/test/java/com/revature/cardealer/CarDealershipCharacterizationTest.java` | Legacy behavior | Modern authenticated flow; original historical failure expectations unchanged in source master |
| `src/test/java/com/revature/cardealer/OfferCharacterizationTest.java` | Legacy defects | Modern stable/atomic inventory behavior and CI parity |
| `src/test/java/com/revature/service/RoleAuthorizationServiceTest.java` | Permission regression | Preserve deny-by-default, forged/revoked identity and session revision checks |
| `src/test/java/com/revature/service/RoleLoginServiceCharacterizationTest.java` | Legacy owned-vehicle behavior | Modern dynamic immutable ownership/records |
| `src/test/java/com/revature/service/UserLoginServiceCharacterizationTest.java` | User operations | Deny untrusted deletion and retain authenticated/atomic role boundary |

**One identical changed blob**: `src/test/java/com/revature/cardealer/PaymentPlanTest.java`; no file-level collision although complete final tests must still pass.

**Caveat:** a historic short-only file might still require deliberate migration even when its path is not in the table. The [22-case behavioral parity register](CAR-DEALERSHIP-SHORT-BRANCH-BEHAVIORAL-PARITY-2026-10-29.md) covers 6 facade/role, 5 inventory and 11 purchase-review tests. The current isolated candidate [CI #40997446982](https://github.com/danwiz/project0-cardealership/actions/runs/40997446982) passes 346 tests per Java11/17. Neither fact proves a complete Git merge or that all archived short-only business requirements were accepted.

## 4. Offline Git clone/backup and actual merge-tree: BLOCKED HERE

- Local `git ls-remote https://github.com/danwiz/project0-cardealership.git HEAD` was attempted in the execution container and **failed because `github.com` could not be resolved**. Therefore no live Git clone, full `git bundle`, `git fsck` of remote objects, actual `git merge-tree` output, verified restore or independent off-GitHub archive exists yet.
- A **syntax-checked** Bash source-audit helper is saved at [`tools/rehearse-dealership-source-merge.sh`](tools/rehearse-dealership-source-merge.sh) and available as a separate local copy in the conversation. The helper refuses a nonempty destination, performs full `git clone --mirror`, checks all three exact branch heads against their pinned SHAs, runs `git fsck`, exports refs/tree lists and a self-contained all-ref `git bundle` plus SHA-256 and bundle verification, then runs **two non-destructive remote-ref `git merge-tree --write-tree` rehearsals** (master/candidate and short/candidate), recording exit codes and outputs. It does **not** push to GitHub. This helper has **not** been executed end-to-end against the live repository.
- The bundle captures Git refs/objects only, **not** GitHub PR bodies, reviews, discussion threads, CI artifacts, Git LFS media, deployment secrets, licenses approvals or external provenance. A real operational archive requires these additional authorized exports, separately stored and verified.

## 5. Stage and acceptance record

| Gate | Current status |
| --- | --- |
| Exact complete five-tree source screening | **VERIFIED** (`truncated=false`) |
| 7 master-distinct and 15 short-distinct file inventory | **VERIFIED AS BLOBS, NOT CONFLICT HUNKS** |
| Legacy PBKDF2 current candidate parity | **VERIFIED**, 346-test workflow |
| Two short add/add resolutions | **PROPOSED**, not merged |
| Actual `git merge-tree` rehearsal | **NOT EXECUTED**; network blocked |
| Full off-GitHub Git bundle and restore proof | **NOT EXECUTED**; network blocked |
| Canonical repo owner signoff | **PENDING** |
| Production release / schema / issuer-writer trust | **NO-GO** |

**Do not downgrade the main [17-gate release register](CAR-DEALERSHIP-RELEASE-GATE-REGISTER-2026-10-29.json) based on this screening.** Original branches and all draft PRs stay unchanged.
