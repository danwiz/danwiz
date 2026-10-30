# Car Dealership — Verified Historical Git Archive and Three-Ancestry Reconciliation

**Execution date:** 2026-10-30 EDT  
**Status:** independently verified historical archive; reproducible LOCAL ancestry proposal; production promotion **NO-GO**.

## 1. Independent historical Git archive and custody

**Source repo:** `danwiz/project0-cardealership` (public). A read-only source archival workflow was committed only to the unmerged integration branch, commit `6db63674d0ab4ddfa93470d3ff38c98695dbf122`.

**Actual archive workflow:** [GitHub Actions #41047811594](https://github.com/danwiz/project0-cardealership/actions/runs/41047811594) **SUCCESS**; temporary GitHub artifact `public-dealership-full-git-bundle`, ID `12972524130`, retention **one day**. The workflow performed mirror clone, pinned source-head checks, `git fsck --full --strict`, `git bundle create --all`, `git bundle verify`, a fresh restored checkout and its own `git fsck`.

**Uploaded file:** `project0-cardealership-full-git-history-2026-10-30-verified.zip` in personal OneDrive → GitHub → GitHub Engineering & Open Source → 13 Source Archive & Evidence → project0-cardealership — Historical Git Archive.
- [Verified private OneDrive archive](https://onedrive.live.com?cid=0F85277D99DDE0A6&id=F85277D99DDE0A6!s4c844c1d298e45fcbc05a28a17672551) — file item `F85277D99DDE0A6!s4c844c1d298e45fcbc05a28a17672551`.
- **ZIP size:** 1,058,812 bytes.
- **ZIP SHA-256:** `ffe2ce7fc9b4ce0c78743a8437e4fd2d50ae06ddb27eeb2f402253384a1d7b7d`.
- **Contained Git bundle size:** 1,112,489 bytes.
- **Contained Git bundle SHA-256:** `41ad1f09a546d1fac8c9e850a5f00739b92443d971dd43535238969433113ff3`.

**Independent verification outside GitHub:** downloaded the workflow artifact to an isolated local working directory, validated archive paths, performed `sha256sum -c` on the inner bundle, independently ran `git bundle verify` in a new bare Git repo, cloned a new mirror from the bundle, and passed `git fsck --full --strict`. The restored archive contains **296 refs** and **680 commits reachable from those refs** (no local Git tags), with verified:
- protected `master`: `90741d3abe51d9cc002aaeb1dacae27b933fba10`;
- short branch #84: `086fbf91294f74fe4bd967256498ef94e92c501a`;
- frozen tested modernization source: `0cbad314956ad1d36542d30afa6519a1bbfecdce`;
- historical archive workflow commit: `6db63674d0ab4ddfa93470d3ff38c98695dbf122`.

**Independent cloud readback:** the uploaded OneDrive item was listed from its actual parent and fetched again via Microsoft Graph item ID. SHA-256 of the **re-downloaded cloud ZIP** is exactly `ffe2ce7fc9b4ce0c78743a8437e4fd2d50ae06ddb27eeb2f402253384a1d7b7d`, byte-for-byte equal to the original downloaded artifact. This demonstrates custody and integrity of the off-GitHub copy; the backup is **not merely a link to a GitHub artifact**.

**Parallel Google Drive destination:** existing private `GitHub Engineering & Open Source / 13 Source Archive & Evidence` folder discovered; project subfolder created at [Google Drive](https://drive.google.com/drive/folders/1QLcG8zbX36EsLd9MzZnO17WzTJgnhXqr). The Google Drive binary-upload connector rejected the structured file reference (input schema mismatch). **No Google Drive ZIP upload is claimed.**

**Archive limits:** this is all *advertised Git refs/objects reachable at the captured time*. It does **not** capture Git LFS payloads if any, GitHub PR/issue reviews, protected environment configuration, Actions job logs, repository secrets, contributor permission history or legal license permissions. Future Git changes require refreshed backups and custody checks. No source/license/secret provenance acceptance has been signed.

## 2. Real local short/candidate merge from restored independent Git bundle

Using **only** the independently restored bundle, a disposable local worktree was created at frozen candidate `0cbad314956ad1d36542d30afa6519a1bbfecdce` and `git merge --no-ff --no-commit` applied short `086fbf91294f74fe4bd967256498ef94e92c501a`.

**Actual result:** Git returned conflict status and exactly **15 unmerged paths**, matching the prior [read-only Actions merge-tree evidence](CAR-DEALERSHIP-CONFIRMED-MERGE-TREE-REHEARSAL-2026-10-30.md).
- For this **technical proof only**, all **15 explicitly enumerated** conflicting paths were individually selected from the validated candidate (not a global `-X ours` merge strategy).
- The automatically merged result still introduced **exactly nine additional paths** from the short branch, with 671 lines of net additions:

| Category | Short-only paths added by a blind merge |
| --- | --- |
| Historical design notes | `docs/ADMIN-BOOTSTRAP-THREAT-MODEL.md`; `docs/PURCHASE-INTEGRITY-REVIEW.md` |
| Incompatible legacy runtime | `src/com/revature/service/AuthorizedInventoryService.java`; `AuthorizedPurchaseReviewService.java`; `LegacyOfferPurchaseInventoryAdapter.java`; `PurchaseInventoryPort.java` |
| Original branch-specific tests | `src/test/java/com/revature/cardealer/CarDealershipRoleRevalidationTest.java`; `src/test/java/com/revature/service/AuthorizedInventoryServiceTest.java`; `AuthorizedPurchaseReviewServiceTest.java` |

- Each added path was explicitly removed **from the disposable local merge output only**, not from the preserved source branch or Git bundle. The original paths remain fully available in short #84 and in the off-GitHub archive.
- The resulting local **two-parent** short+cand merge commit is `cbe283d5fb0fd0b885f6a3abdeeaa744096c5464`. Its parents are exact candidate `0cbad314...` and short `086fbf912...`.
- **Resulting Git tree SHA:** `c2887034b4ef819f1d0429a25a024c6a1acb35ac`, **identical to frozen candidate**, with **zero source differences**.

**This proves a possible historical ancestry reconciliation without restoring unsafe old purchase paths.** It does not mean owner approval to omit any nine source files, accept the behavioral substitutions, or merge short into a production/release branch. The [original nine-file disposition register](CAR-DEALERSHIP-SHORT-ONLY-SOURCE-DISPOSITION-AND-LOGIN-TAG-REVIEW-2026-10-30.md) remains proposed.

## 3. Real local three-ancestry merge from restored bundle

On the local short+cand commit above, the protected historical master SHA `90741d3abe51d9cc002aaeb1dacae27b933fba10` was merged with `git merge --no-ff --no-commit`. Git returned **exactly six** source conflicts, matching the prior Actions analysis.

The six paths were explicitly selected from the candidate-side local merge. The formerly auto-merged `UserLoginServiceCharacterizationTest.java` was **deliberately restored from the frozen candidate blob** to preserve uppercase `SECURITY` tags and fail-closed account deletion. The local Git index had no unmerged entries, and `git diff` against the tested candidate was empty.

| Record | Local-only SHA |
| --- | --- |
| Short+cand intermediate two-parent merge commit | `cbe283d5fb0fd0b885f6a3abdeeaa744096c5464` |
| Three-ancestry final local merge commit | `a06d6190909ebb46848e6b7e3f0150121885a1cb` |
| Final commit first parent | `cbe283d5fb0fd0b885f6a3abdeeaa744096c5464` |
| Final commit second parent | `90741d3abe51d9cc002aaeb1dacae27b933fba10` |
| **Final Git tree SHA** | **`c2887034b4ef819f1d0429a25a024c6a1acb35ac`** |
| Tested source candidate Git tree SHA | **`c2887034b4ef819f1d0429a25a024c6a1acb35ac`** |
| `git fsck` local three-ancestry history | **PASS** |
| Combined source change compared with candidate | **ZERO files** |

The **local three-ancestry source content is exactly identical** to the previously validated candidate code. The existing [Java 11/17 PostgreSQL 16 build and SECURITY-tagged test evidence](CAR-DEALERSHIP-CORRECTED-SECURITY-TAG-MERGE-CI-2026-10-30.md) establishes correctness of the *identical source tree*, but **the new local three-ancestry commit itself was not tested by CI or published as a remote ref**. GitHub workflows, branch policy and release approval could depend on ancestry/trigger context and must be retested if promoted.

## 4. Release governance and next decisions

1. **Technical archive creation and offline restore: VERIFIED. OneDrive off-GitHub custody and byte-for-byte reread: VERIFIED.** A second Google Drive copy remains pending connector repair, and evidence retention/revalidation still needs an archival policy.
2. **Technical source ancestry reconciliation: VERIFIED LOCALLY.** This includes exact 15+6 conflicts, short-only additions excluded in the proof, safe characterization test and byte-identical resulting source tree. **No code/history was pushed.**
3. **Owner and independent reviewer consent: NOT GIVEN.** Nine short-only file dispositions and all 15/6 conflict choices require approval; source provenance and license permissions must be verified.
4. **Canonical Maven destination: UNAPPROVED.** Separate Java source layout/JUnit/persistence port requires new final SHA and CI.
5. **Production readiness: NO-GO.** SQL issuer/writer/reconciler authentication, PostgreSQL crash/failover/replica-lag recovery, security review, credential migration controls and disaster-recovery signoffs remain unverified.

**Do not mark the entire G01 or G02 gate closed merely because technical substeps pass.** The original 17-gate register should retain its overall NO-GO status until owner-signed source provenance, conflict decisions, final durable reviewed PR, independent security and production gates are satisfied.

No protected branches, draft PRs, production databases, deployments, authentication secrets or releases were modified by this offline analysis.
