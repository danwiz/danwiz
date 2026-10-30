# Car Dealership — Disposable Master+Candidate Merge Verification

**Capture:** October 30, 2026 ET  
**Evidence:** [GitHub Actions run #41002545989](https://github.com/danwiz/project0-cardealership/actions/runs/41002545989) — **COMPLETED SUCCESS** for both Java 11 and Java 17.  
**Workflow version:** isolated branch-only `.github/workflows/disposable-master-integration-verification.yml` at commit `755a46aef24c9ea8a254e958e0a7dc8a9d76e45b`.  
**Scope:** real **ephemeral CI-runner merge**, never pushed to GitHub or added to a protected/default branch.  
**Release decision:** **NO-GO**.

## 1. Exact merged source content and parentage

| Field | Verified from independent JDK runner text artifacts |
| --- | --- |
| First parent, protected historical `master` | `90741d3abe51d9cc002aaeb1dacae27b933fba10` |
| Second parent, original 346-test source candidate | `0cbad314956ad1d36542d30afa6519a1bbfecdce` |
| **Final merged Git tree** | **`e21385cea6cd9969c3203cb65d739ba71bda04bc`** |
| Ephemeral Java 11 merge commit | `01608f7d6aa37d806b0b0aac477b27bcd54894dd` |
| Ephemeral Java 17 merge commit | `9f9e7ca83ba1ff05344b286e4a8ae1f6d126a80c` |
| Explicit conflict resolutions | Six named `master`-side files resolved individually from candidate side |
| Unmerged stage entries after resolution | **None** |
| New whitespace introduced vs pinned source candidate | **None** |
| Automatically merged path different from candidate | `src/test/java/com/revature/service/UserLoginServiceCharacterizationTest.java` |

The **two temporary Git commit IDs differ** because each runner made an independent local commit; critically, their **tree SHA is identical**, proving the combined file contents were identical. These merge commits existed only in disposable GitHub-hosted runners and are **not accessible as promoted GitHub refs**. The integrated source tree SHA is a reproducible content identifier, not an approved release tag or production commit.

## 2. Exact conflict-resolution and verification procedure

The workflow performed:
1. `actions/checkout@v5` with `fetch-depth:0`, `persist-credentials:false` and `permissions: contents:read`.
2. SHA fence against protected source `master`, the 346-test modernization candidate and their real merge base.
3. `git switch -c disposable/master-candidate <master SHA>`; a genuine `git merge --no-commit --no-ff <candidate SHA>`, with expected conflict exit and **six unmerged paths** verified.
4. Individual `git checkout --theirs -- <path>` **only for the six explicitly reviewed conflict paths**, rather than global `-X theirs` or blanket file replacement:
   - `.github/workflows/maven-ci.yml`
   - `src/test/java/com/revature/DAOService/DAOServiceCharacterizationTest.java`
   - `src/test/java/com/revature/cardealer/CarDealershipCharacterizationTest.java`
   - `src/test/java/com/revature/cardealer/OfferCharacterizationTest.java`
   - `src/test/java/com/revature/cardealer/PaymentsCharacterizationTest.java`
   - `src/test/java/com/revature/service/RoleLoginServiceCharacterizationTest.java`
5. Verified the actual local commit had **exactly the two pinned parents**. Uploaded text-only commit/tree/diff/provenance reports; did **not** publish the Git objects or a full Git bundle.
6. Set disposable PostgreSQL 16 logical-WAL configuration and ran `mvn --batch-mode --no-transfer-progress clean verify` against the locally merged tree on Java 11 and 17.

This procedure *tests a proposed* master-conflict strategy. It does not represent owner-signed acceptance of the six file choices or of the automatic merge.

## 3. Test verdict from actual merged ancestry

| Runtime | Total tests | Failures | Errors | Skipped | Maven |
| --- | ---: | ---: | ---: | ---: | --- |
| Java 11 / isolated PostgreSQL 16 | **346** | 0 | 0 | 0 | **BUILD SUCCESS** |
| Java 17 / isolated PostgreSQL 16 | **346** | 0 | 0 | 0 | **BUILD SUCCESS** |

**Run:** [#41002545989](https://github.com/danwiz/project0-cardealership/actions/runs/41002545989). Both jobs completed SUCCESS. The [previous source candidate #40997446982](https://github.com/danwiz/project0-cardealership/actions/runs/40997446982) also passed 346/JDK with two diagnostic jobs, but it lacked actual `master` merge ancestry. This new rehearsal is distinct evidence.

Text-only artifact references, both independently downloaded and inspected:
- Java 11: [artifact #12953144849](https://github.com/danwiz/project0-cardealership/actions/runs/41002545989/artifacts/12953144849), downloaded ZIP SHA-256 `da2f4cf1137938e530d75388322032c59217618f87c1bee27b8ffc86400b6ba2`.
- Java 17: [artifact #12954415227](https://github.com/danwiz/project0-cardealership/actions/runs/41002545989/artifacts/12954415227), downloaded ZIP SHA-256 `6e06a1d3eccd8ad40d9e297fe48fe6bd92c4f44379da66c8cd643540ddb151e6`.

Both artifact `auto-merge-vs-candidate.txt` files list **one modified path only**: `UserLoginServiceCharacterizationTest.java`. This automatically merged test passed but still needs semantic review before final promotion.

## 4. Diagnostic attempt history and source hygiene

The first two draft CI-only merge tests were not accepted as a success:
- [#41002248325](https://github.com/danwiz/project0-cardealership/actions/runs/41002248325) **FAILED before actual conflict resolution**: Git's merge operation required a local committer identity. Corrected by applying local-only `git config user.name/user.email` inside the disposable runner, not a global config or GitHub auth token.
- [#41002371721](https://github.com/danwiz/project0-cardealership/actions/runs/41002371721) **FAILED after conflict resolutions** on repository-wide `git diff --cached --check` due to two pre-existing source whitespace findings. The workflow now preserves those findings separately and checks only **new whitespace relative to the verified candidate** (clean).

**Previously existing and not silently modified:**
1. `docs/security/postgresql-writer-epoch-transaction-fence.md`, line 41 — trailing whitespace.
2. `src/test/java/com/revature/application/TestDecodingAuditSource.java`, line 57 — trailing whitespace.

These are documentation/code-hygiene cleanup candidates, not proven functional/security regressions. Fix separately with source review; do not alter historical files purely to manufacture a green ancestry test.

## 5. Distinguish merged master from competing short branch

This rehearsal **resolved only the six actual conflicts with historical `master`**. The four-PR competing short branch (#78/#82/#83/#84) was **not actually merged**; its **15 merge-tree conflicts** and non-conflicting short-only source remain an explicit architecture and provenance decision. The [22-case behavioral parity register](CAR-DEALERSHIP-SHORT-BRANCH-BEHAVIORAL-PARITY-2026-10-29.md) tests selected modern equivalents but does **not** add the short branch as a Git parent or validate every preserved legacy service.

The source candidate and this derived merged tree still require owner/DBA/security approval; there is **no final source PR or Maven destination promotion**, no signed archive/restore, no physical PostgreSQL failover or independently provisioned production issuer/writer/reconciler, no final license/SBOM verdict and no approved rollback.

## 6. Updated stage gate

| Gate | Verified now | Still missing |
| --- | --- | --- |
| Exact full-history merge-tree conflicts | **6 master + 15 short, confirmed** | Independent reviewer dispositions |
| Six-file master conflict strategy | **Real local two-parent merge + same tree SHA twice + 346/JDK pass** | Publish only to authorized review branch after provenance/ADR; independent review |
| Automatic master test-file merge | **Test suite passed** | Human review of the mixed `UserLoginServiceCharacterizationTest` content |
| Short branch | **Behavior test mapping and 15 confirmed collisions** | Decide whether any additional short-only code/contracts need inclusion |
| Independent historical Git backup | **No** | Off-GitHub bundle, checksum, restore proof and custody |
| Production release | **NO-GO** | All remaining 17-gate acceptance requirements |

This is the first **passing executable master-ancestry integration prototype**, **not** a ready-to-merge or production release. The protected source `master` is unchanged.


## 7. Current isolated branch CI also passed after diagnostic workflow commits

The source integration branch's latest head `755a46aef24c9ea8a254e958e0a7dc8a9d76e45b` (adds only diagnostic workflows since original pinned source candidate) independently passed [normal Maven CI #41002545986](https://github.com/danwiz/project0-cardealership/actions/runs/41002545986): **Java 11 and Java 17 each 346 tests, 0 failures/errors/skips**, both Maven test/verify BUILD SUCCESS, plus **both diagnostics jobs success**. This corroborates that the audit-only workflow commits did not disturb the existing source CI.

**Keep distinct:** the normal Maven CI run tests branch head `755a46...`; the *disposable actual master/candidate two-parent merge* is independently tested by run `#41002545989` and creates tree `e21385...`. Neither is a published or accepted product release.
