# Car Dealership — master baseline provenance and integration preservation manifest

**Capture date:** 2026-10-29 ET (GitHub live source reads)  
**Source repository:** `danwiz/project0-cardealership`  
**Immutable source commit:** [`90741d3abe51d9cc002aaeb1dacae27b933fba10`](https://github.com/danwiz/project0-cardealership/tree/90741d3abe51d9cc002aaeb1dacae27b933fba10) — checked via GitHub branch API, `master` **protected**.  
**Integration under test:** `security/integration-candidate-master-pbkdf2-parity-20261029`, latest CI-triggering commit `0cbad314956ad1d36542d30afa6519a1bbfecdce`.  
**Status:** preservation/indexing and source-level integration decisions, **not a merge/release or production acceptance**.

## Nine `master`-side changed paths

The following files changed on the `master` side of the common ancestry compared with the long development candidate. **File-level Git blob SHAs** were independently read from the actual source commit and the candidate; the equal source and candidate PBKDF2 blobs are a stronger parity check than comparing commit counts.

| Path (prefix `src/test/java/` or `src/` where shown) | Exact `master` blob SHA | Integration candidate blob | Disposition |
| --- | --- | --- | --- |
| `.github/workflows/maven-ci.yml` | `20b37da0babdf076898557afa52827d8a179d3f4` | `06606f360f93efb751dbe583aab176150d9f7360` **before Phase 10 workflow edit** | **RECONCILE** master push trigger and downloadable Maven diagnostics into PG16/Java11/17 matrix |
| `src/com/revature/service/Pbkdf2PasswordHasher.java` | `fe47ab27572523fa1047443c4090ed758891e5c5` | **same blob** | **PRESERVED exactly** — 600k PBKDF2 work factor, bounded verifier, fixed salt/output lengths |
| `src/test/java/com/revature/service/Pbkdf2PasswordHasherTest.java` | `ceec0a5db502d597b5626775bdc6463194b9703e` | **same blob** | **PRESERVED exactly** — 4 tests including hostile work-factor regression |
| `src/test/java/com/revature/DAOService/DAOServiceCharacterizationTest.java` | `8e53b37d1e2dc4a6f26ba5ddf9c97a01561ea146` | `e9b7cd2588ee30b075c9fc435a6eaeb765bb68c6` | Historical double .dat filename + null result behavior preserved in source commit; modern DAO uses explicit status and bounded filters |
| `src/test/java/com/revature/cardealer/CarDealershipCharacterizationTest.java` | `f3b3ca38b07ec4c74875fda6de903c24f8abe4c4` | `ee2a5a2d0f59b2a3072b8c9878e4a872a817150f` | Historical unsafe customer cast/menu string identity/null dereference recorded; current command denies no-actor persistence and verifies role |
| `src/test/java/com/revature/cardealer/OfferCharacterizationTest.java` | `46800704393aa0b809a48a5c8ab255e0c19d560c` | `0019d59a01db0219c32559ec4ae044e0ec557f81` | Historical pending-offer list defects recorded; modern tests require stable IDs, single winner, bounded inventory and complete rejection |
| `src/test/java/com/revature/cardealer/PaymentsCharacterizationTest.java` | `5cae95cd414b9b04c048fb1f47a941598953987d` | `b24ee2907e6bb8b114ca4022ef1cffc91682d2d0` | Historical negative balance/fixed-capacity defects recorded; modern tests require attributed transactions, no overpay and unbounded list |
| `src/test/java/com/revature/service/RoleLoginServiceCharacterizationTest.java` | `e982322e0c1222cdbe264dab675cd053fff75c45` | `f4b11edfc2d8eb40a01e2ca3d4259582576b18cd` | Historical 20-owner limit and null slot failure documented; modern tests require dynamic immutable ownership views and correct payment attribution |
| `src/test/java/com/revature/service/UserLoginServiceCharacterizationTest.java` | `9a9409a5744eac5b031d3c4de1b24f62b9881dfe` | `e7074cf0ca4db2fab3a434dce0f8ec96c19da537` | Historical unrestricted `removeUser` test replaced by `unauthenticatedDeletionFailsClosed`; preserve historical intent, not unauthorized deletion |

For each historical file, the original content remains retrievable using the pinned URL template:

`https://github.com/danwiz/project0-cardealership/blob/90741d3abe51d9cc002aaeb1dacae27b933fba10/<path>`

Do **not** replace these source objects with modernized tests. Git file history and the source commit are the reference for the original academic/training behavior. This manifest is not an independent offline byte backup, and integrity preservation should also include an eventual trusted Git bundle or archival checksum export outside GitHub.

## Method-level decisions for six changed historical characterization suites

| Historical test intent on `master` | Modern expected behavior and verification |
| --- | --- |
| DAO `createData` appends `.dat` twice in some cases; missing file returns null | Modern DAO roundtrips an exact supplied filename, returns explicit `NOT_FOUND`, filters deserialization and fails closed on invalid input |
| Customer registration fails unsafe downcast; menu comparison uses string reference identity | Modern customer registration succeeds, role-based console routing uses value equality and an authenticated administrator boundary |
| Legacy offer/report can hit array index errors; rejecting entries leaves later pending requests | Modern inventory uses stable request identifiers, immutable views and complete state transitions; JDBC approval is atomic |
| Legacy payments allow negative outstanding balance and fail after 20 records | Modern transaction ledger prevents overpayment and handles larger histories while attributing customer and ownership |
| Legacy ownership list fails at index 20 and when rendering a null slot | Modern customer ownership is dynamically sized, immutable in read views, and safe for empty slots |
| Historical user deletion allows direct unprivileged removal of registered account | Modern account repository and operator boundaries must deny unauthenticated account deletion, retaining strict session revision revocation |
| Legacy work-factor validation on `master` | **Identical** source and four negative/password roundtrip tests on candidate; new hash policy remains 600k |

## CI reconciliation change under validation

Candidate workflow commit [`0cbad314956ad1d36542d30afa6519a1bbfecdce`](https://github.com/danwiz/project0-cardealership/commit/0cbad314956ad1d36542d30afa6519a1bbfecdce) explicitly restored:
- `master` to `push.branches` (candidate previously omitted it, although `pull_request.branches` already included it);
- the separate `diagnostics` job from master, using current `actions/download-artifact@v6`;
- existing Java 11/17, disposable PostgreSQL 16, security/strategy branch coverage, `contents: read`, and Maven failure diagnostics.

**Validation is pending:** [Actions run #40997446982](https://github.com/danwiz/project0-cardealership/actions/runs/40997446982) on the exact candidate commit. A green run on the isolated branch does not itself test an actual push to protected `master`, because no such push is authorized or performed.

## Release-level reconciliation gates

1. Verify the workflow's new Java11/17 `verify` and independent `diagnostics` jobs complete successfully on the exact head; inspect log uploads and avoid silently dropping failure diagnostics.
2. Run master characterization tests against the preserved master source in an **archival or pre-change verification workflow**, not against modern code expecting intentionally fixed bugs. Copying or rewriting tests into the modern suite could conceal changes in meaning.
3. Confirm all nine master-side paths received explicit code, test or preservation disposition and that other master-only commits contain no unseen runtime/CI changes.
4. The full repository still has 16 master-exclusive commits, 91 competing draft PRs, and a canonical Maven destination decision pending. **This manifest does not merge those commits or settle the destination.**
5. Preserve legal provenance/licensing, avoid checked-in build artifacts, and require independent code/DBA/security review plus acceptance of missing PostgreSQL failover and issuer/writer/reconciler gates.

**Current release decision: NO-GO.** No master/default merge, no production SQL/deployment/credential work, no Maven repository import, no published release.
