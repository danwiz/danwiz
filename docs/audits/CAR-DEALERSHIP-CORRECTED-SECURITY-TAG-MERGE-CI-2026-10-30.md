# Car Dealership — Corrected seven-path disposable master integration

**Execution:** October 30, 2026 ET  
**Authoritative CI:** [GitHub Actions #41004555990](https://github.com/danwiz/project0-cardealership/actions/runs/41004555990) — **COMPLETED SUCCESS**, Java 11 and Java 17.  
**Diagnostic workflow commit:** `dc1e596bb9efbe610bb6beedbf09a76184adb59c` (existing unmerged isolated candidate branch only).  
**Protected source master:** `90741d3abe51d9cc002aaeb1dacae27b933fba10` (not modified).  
**Second parent, frozen tested code candidate:** `0cbad314956ad1d36542d30afa6519a1bbfecdce`.  
**Resulting identical Git tree:** **`c2887034b4ef819f1d0429a25a024c6a1acb35ac`**, independently verified by both runner artifacts and the original candidate's Git commit tree API.  
**Status:** reproducible **disposable** merge plus exact-content and test proof; **not** an accepted source PR/branch merge, canonical Maven import or production release.

## Root cause of the prior automatic merge discrepancy

The first [master/candidate disposable CI #41002545989](https://github.com/danwiz/project0-cardealership/actions/runs/41002545989) resolved six actual Git content conflicts from the candidate side; Git automatically combined a seventh dual-changed file, `UserLoginServiceCharacterizationTest.java`, yielding tree `e21385cea6cd9969c3203cb65d739ba71bda04bc` that passed all 346 tests. That file combined **the safe `unauthenticatedDeletionFailsClosed` assertion** with **two lowercase master-sourced JUnit annotations** `@Tag("security")` and `@Tag("target-behavior")`. Their capitalization differs from the candidate's `SECURITY` / `TARGET-BEHAVIOR` tags; exact tag filters are case-sensitive and could silently omit these tests.

**Corrected proposed resolution:** explicitly restore `UserLoginServiceCharacterizationTest.java` from original candidate blob `e7074cf0ca4db2fab3a434dce0f8ec96c19da537`, verify its hash, check for uppercase security tag and `unauthenticatedDeletionFailsClosed`, and reject any revival of permissive `removeUserMakesPreviouslyRegisteredUserUnavailable` expectations. Keep the six originally conflicting paths resolved individually as before. **No wholesale `-X theirs` was used**.

The resulting merged **tree now exactly matches the frozen tested candidate's tree**, `c2887034b4ef819f1d0429a25a024c6a1acb35ac`. It still has **two legitimate Git commit parents** in the local CI runner (master and the source candidate), proving a reproducible source merge operation without changing the validated source content.

## Actual Java 11 / Java 17 acceptance evidence

| Check | Java 11 | Java 17 |
| --- | --- | --- |
| Workflow job result | SUCCESS | SUCCESS |
| Unit/integration test count | **346** | **346** |
| Failures / errors / skips | **0 / 0 / 0** | **0 / 0 / 0** |
| Maven `clean verify` | BUILD SUCCESS | BUILD SUCCESS |
| Git merged tree SHA | `c2887034b4ef819f1d0429a25a024c6a1acb35ac` | Same |
| Runner-only merge commit | `1bbb0378b6c0970e1d6a157562be114ae4847485` | `415772062f98687961d5e297449c149190ea933c` |
| Text artifact ID | `12954856814` | `12954549007` |
| Downloaded ZIP SHA-256 | `3ccd110e7124555c26643fe002e362f4bb407ea219c355655587fa6e7a95530c` | `ca72a8338fb64eafe04bc7724bdb307ffe86bea343da13903becd219b19b3c73` |

Artifact links: [Java 11](https://github.com/danwiz/project0-cardealership/actions/runs/41004555990/artifacts/12954856814) and [Java 17](https://github.com/danwiz/project0-cardealership/actions/runs/41004555990/artifacts/12954549007).

Both actual artifact `auto-merge-vs-candidate.txt` files are **empty**: there is **no file content difference** compared with the source candidate tree. The `git diff --cached --check` output preserved two **pre-existing** trailing whitespace findings in unrelated candidate files, and `new-whitespace-warnings.txt` is empty in both. No evidence was suppressed; no source/Docs code was changed to hide them.

**Attempt trace:** an intermediate run [#41004391593](https://github.com/danwiz/project0-cardealership/actions/runs/41004391593) failed before the local merge because its SHA fence still pointed to a prior workflow revision. The fence was refreshed to the correct prior head; the successful run is #41004555990. This was CI harness configuration, not an application test failure.

## What is and is not complete

**Verified:** six real master content conflicts resolved locally, plus a deliberate semantic correction of one auto-merge; resulting content exactly equals previously accepted *candidate code*; Java 11/17 + disposable PostgreSQL 16 with 346 real tests each. Source lineage and exact content now independently reproducible.

**Outstanding:** nine short-only file decisions and 15 true short-branch merge conflicts are **reviewed but owner-unapproved**. Historical independent off-GitHub Git archive and restore proof, source licensing, signed canonical Maven destination ADR, production PostgreSQL physical failover and principal boundaries, release rollback and independent QA/DBA/security signoff are still missing. No durable approved merge-commit branch ref was created, and no production or protected branch mutation occurred.

**Release register:** 17 gates, 12 still blocking, `release_authorized=false`, `disposition=NO-GO`. [Machine-readable register](CAR-DEALERSHIP-RELEASE-GATE-REGISTER-2026-10-29.json).


## Additional ordinary branch-head CI after the workflow change

The isolated source branch at workflow commit `dc1e596bb9efbe610bb6beedbf09a76184adb59c` additionally passed [normal four-job Maven CI #41004556161](https://github.com/danwiz/project0-cardealership/actions/runs/41004556161): Java 11 and 17 each **346 tests, zero failures/errors/skips**, with both independent Maven diagnostics jobs **SUCCESS**. This is separate from the corrected actual disposable master/modernization merge CI #41004555990, which has both local merge parents and identical validated source-tree SHA. Neither test run grants production or source-integration approval.
