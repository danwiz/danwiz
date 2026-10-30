# Car Dealership — Confirmed Git Merge-Tree Rehearsal Results

**Execution:** GitHub Actions [run #41001881391](https://github.com/danwiz/project0-cardealership/actions/runs/41001881391) (2026-10-30 04:15 UTC)  
**Job:** `Non-destructive Git merge-tree inspection` — **COMPLETED SUCCESS**  
**Commit containing the diagnostic workflow:** `e4b21e123d443079be2ccffd826a62c5d64f0c49`  
**Comparison candidate:** frozen **CI-tested** source SHA `0cbad314956ad1d36542d30afa6519a1bbfecdce` (not the added workflow commit).  
**Protected historical master:** `90741d3abe51d9cc002aaeb1dacae27b933fba10`.  
**Competing short branch:** `086fbf91294f74fe4bd967256498ef94e92c501a`.  
**Status:** **Actual Git merge-tree conflict evidence verified**. **Not a merged integration candidate, code review, archival bundle or production approval.**

## 1. Execution integrity

GitHub-hosted runner used `actions/checkout@v5` with `fetch-depth: 0`, `persist-credentials: false` and workflow `permissions: contents: read`.

The runner independently checked the exact pinned master/short branch commits and verified both source ancestry merge bases:
- Master/candidate merge base: `9c242f9880a18a7749621a6ed5f6d53d3ee5fcdc`.
- Short/candidate merge base: `ad8d03574c7f048b236c9d24f0c03ac54dffcbd7`.

`git fsck --full --strict` **completed successfully** (empty diagnostic log), and two **real** `git merge-tree --write-tree` operations were performed on the complete Git object graph.

Runner results were uploaded as a **text-only** GitHub Actions artifact:
- Artifact name: `dealership-read-only-merge-rehearsal`; GitHub artifact ID **12953981471**.
- [Artifact in run](https://github.com/danwiz/project0-cardealership/actions/runs/41001881391/artifacts/12953981471).
- Downloaded archive SHA-256: `efd649e93fc5d7e33eb1947de742b961125012fdd85e7425050d58f0d376fd3b`; the GitHub job upload log advertises the same SHA-256 digest.
- Archive contains 14 text files: SHA/checkpoint evidence, all Git refs, `git fsck` output, both merge-tree outputs, complete conflict lines, source path changes, Git version and a scope README. **No source Git bundle or secrets were uploaded.**

**Critical interpretation:** The Actions job succeeded because the merge rehearsal completed and all expected conflicts were captured. Each `git merge-tree` itself returned **exit code 1**, meaning **CONFLICTS PRESENT**. There was **no clean merge**.

## 2. Exact master → candidate merge rehearsal

`git merge-tree --write-tree 90741d3abe51d9cc002aaeb1dacae27b933fba10 0cbad314956ad1d36542d30afa6519a1bbfecdce`

- **Exit:** `1` (conflicts)
- **Virtual uncommitted tree:** `22cbcc6c394c1ff0be28d763b19e89b3df8e6f7c` (**NOT a release commit**)
- **Six true content-conflict paths:**

| # | Conflict file | Proposed future resolution |
| --- | --- | --- |
| M-01 | `.github/workflows/maven-ci.yml` | Retain candidate's four-job PG16 and Java11/17 workflow, master push trigger and independent diagnostic jobs |
| M-02 | `src/test/java/com/revature/DAOService/DAOServiceCharacterizationTest.java` | Retain corrected explicit file/result handling; original broken behavior SHA-pinned as evidence |
| M-03 | `src/test/java/com/revature/cardealer/CarDealershipCharacterizationTest.java` | Retain verified role checks and safe console behavior |
| M-04 | `src/test/java/com/revature/cardealer/OfferCharacterizationTest.java` | Retain corrected bounded/single-winner inventory request behavior |
| M-05 | `src/test/java/com/revature/cardealer/PaymentsCharacterizationTest.java` | Retain safe payment ledger/no-overpay behavior |
| M-06 | `src/test/java/com/revature/service/RoleLoginServiceCharacterizationTest.java` | Retain modern owner/payment authentication behavior |

`src/test/java/com/revature/service/UserLoginServiceCharacterizationTest.java` was one of the seven dual-different Git blobs in previous screening, but **Git automatically merged it without a textual conflict**. It still requires a final test and behavior review because an automatic merge is not a semantic correctness guarantee.

`Pbkdf2PasswordHasher.java` and its test already have **identical** master/candidate blobs, preserving 600k defaults and bounded validation.

## 3. Exact short → candidate merge rehearsal

`git merge-tree --write-tree 086fbf91294f74fe4bd967256498ef94e92c501a 0cbad314956ad1d36542d30afa6519a1bbfecdce`

- **Exit:** `1` (conflicts)
- **Virtual uncommitted tree:** `7c13e7ac620bdbf1d9302990d017d68dda676429` (**NOT a release commit**)
- **15 true conflict paths:** 13 content conflicts and 2 add/add conflicts:

| # | Conflict file | Type |
| --- | --- | --- |
| S-01 | `.github/workflows/maven-ci.yml` | content |
| S-02 | `src/com/revature/cardealer/CarDealership.java` | content |
| S-03 | `src/com/revature/cardealer/Offer.java` | content |
| S-04 | `src/com/revature/cardealer/OwnedVehicle.java` | **add/add** |
| S-05 | `src/com/revature/cardealer/PaymentPlan.java` | **add/add** |
| S-06 | `src/com/revature/service/AdminLoginService.java` | content |
| S-07 | `src/com/revature/service/CustomerLoginService.java` | content |
| S-08 | `src/com/revature/service/EmployeeLoginService.java` | content |
| S-09 | `src/com/revature/service/InMemoryUserAccountRepository.java` | content |
| S-10 | `src/com/revature/service/UserLoginService.java` | content |
| S-11 | `src/test/java/com/revature/cardealer/CarDealershipCharacterizationTest.java` | content |
| S-12 | `src/test/java/com/revature/cardealer/OfferCharacterizationTest.java` | content |
| S-13 | `src/test/java/com/revature/service/RoleAuthorizationServiceTest.java` | content |
| S-14 | `src/test/java/com/revature/service/RoleLoginServiceCharacterizationTest.java` | content |
| S-15 | `src/test/java/com/revature/service/UserLoginServiceCharacterizationTest.java` | content |

The candidate `OwnedVehicle` has persistent ownership and normalized contract ID support absent in the short version. `PaymentPlan` has comparable positive-payment/no-overpay validation but also adds serialization behavior. Neither file has been resolved or merged; owner review is required.

## 4. What this clears — and does not

**Cleared as evidence:** actual two-sided Git merge-tree rehearsal was executed on complete pinned source ancestry and conflict paths are now known. The prior **seven/15 blob-disagreement** screening is superseded for *conflict counts* by **six/15 actual merge-tree conflicts**.

**Still blocking release:** conflict **resolution**, preserving and reviewing the complete final merged tree, independent off-GitHub Git bundle/restore, canonical repository approval, PostgreSQL failover and identity architecture, approved credential migration, audit/rate limits, supply-chain/license review and independent QA/DBA/security signoff. G02 remains blocking for **resolution** even though the *diagnostic merge-tree stage* is now verified; G01 independent archival backup remains blocked.

The read-only workflow is installed **on the isolated candidate branch**, which now has one additional diagnostic-only commit. The comparison remains pinned to the earlier 346-test source SHA. The preexisting Maven CI runs separately on the diagnostic workflow commit; do not attribute its outcome to the source merge results.

**No default branch was merged, rewritten, force-pushed, or released.** The recorded trees are intermediate local merge objects, not approved product commits.
