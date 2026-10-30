# Car Dealership — Short-only source disposition and automatic login-test merge audit

**Audit date:** October 30, 2026 ET  
**Repository:** `danwiz/project0-cardealership`  
**Frozen short source:** #84, `086fbf91294f74fe4bd967256498ef94e92c501a`  
**Frozen modern candidate code:** `0cbad314956ad1d36542d30afa6519a1bbfecdce`  
**Protected historical master:** `90741d3abe51d9cc002aaeb1dacae27b933fba10`  
**Scope:** the **nine paths existing only on the competing short side**, plus the **one automatically merged master characterization test**. This is an acceptance/disposition proposal, **not** a completed short-branch merge or a release approval.

## 1. Short-only nine-file disposition matrix

The files below were read from the exact short-branch commit; each historical blob SHA is included to prevent misidentifying a future revision. “Preserve” means **pin original source history and archive design intent**. It does not mean copy the old file verbatim into the modern application.

| ID | Short-exclusive path | Original blob SHA | Proposed decision | Reason / modern equivalent |
| --- | --- | --- | --- | --- |
| SO-01 | `docs/ADMIN-BOOTSTRAP-THREAT-MODEL.md` | `e256769690f2dc93f64f79af9164249b4d30adec` | **Preserve as historical design; map requirements** | Short document explicitly says first-admin bootstrap was design-only/not implemented. Modern `docs/security/administrator-bootstrap.md` describes operator-only CLI, persisted singleton marker and no customer-side role escalation; `AdministratorBootstrapServiceTest` contains persistent/restart, duplicate/rollback and concurrency cases. **Modern CI/test coverage, not production authorization.** |
| SO-02 | `docs/PURCHASE-INTEGRITY-REVIEW.md` | `0d0bd63fbedaa20e5c2b4bc1b494d476951906cc` | **Preserve original threat/failure narrative, reject legacy production claims** | Short document explicitly admits process-only state, non-ACID purchase compensation, public `Offer.setAccept` bypass and crash/reconciliation weaknesses. Modern `docs/security/postgresql-trusted-purchase-writer-design.md` and `JdbcPurchaseApprovalService` supply stronger SQL transactions but **still document unapproved production trust boundaries**. |
| SO-03 | `src/com/revature/service/AuthorizedInventoryService.java` | `8d19c2332c53ea70f7b56edcd795ecabd77381c5` | **Behaviorally supersede; do not transplant** | Old API reauthenticates username/password for every direct `Offer` mutation. Modern context-bound `ManageInventoryCommand`, `ConfiguredDomainAdapter`, `RoleAuthorizationService` use persisted revision/session gate. In-memory and JDBC/H2 tests cover valid staff and denied customer, forged role and revoked staff. |
| SO-04 | `src/com/revature/service/AuthorizedPurchaseReviewService.java` | `65e764e406e59c0bab2cafc73448f1f947756701` | **Do not port mutable compensation implementation** | Stages `OwnedVehicle` before `Offer.acceptWithRollback` and removes it on exceptions. Its `rejectAll`, buyer lookup and approval intentions have modern command/query/JDBC transactional equivalents. Production cannot rely on process-local compensation or direct public Offer mutation. |
| SO-05 | `src/com/revature/service/LegacyOfferPurchaseInventoryAdapter.java` | `bf4cc4c8f554f68f47d0296068395580374831d9` | **Keep as archived compatibility concept** | Adapter delegates purchase to `Offer.acceptWithRollback`, explicitly lacking ACID and crash recovery. Do not insert this adapter as an alternative runtime purchase writer when JDBC transactions and receipts are required. |
| SO-06 | `src/com/revature/service/PurchaseInventoryPort.java` | `56f2719a6c567805b1e9fe0cd6c3ff051a0b3dca` | **Preserve interface intent, not identical class/API** | This single-method port documents approval without promising durability. Current typed `ApplicationPorts.PurchaseApproval` and `ReviewPurchaseRequestCommand` track reviewer and request identifiers; copying the old signature could bypass modern identity/replay controls. |
| SO-07 | `src/test/java/com/revature/cardealer/CarDealershipRoleRevalidationTest.java` | `b1ed0c469e0c358b2e7360d01cb9bf401c5343f7` | **Archive test source; map 6 invariants** | Forged admin, role demotion, deletion, missing identity and direct-persistence checks are mapped to current role/revocation/command tests. Do not restore a legacy static `CarDealership.isCurrentRoleAuthorized` API solely to run historic tests. |
| SO-08 | `src/test/java/com/revature/service/AuthorizedInventoryServiceTest.java` | `6c119490a287f06a75d692138caccf6c5ffb3462` | **Archive 5 cases; modern command regressions CI-covered** | The isolated candidate's `SessionDemotionInventoryRegressionTest` verifies actual authenticated customer/forged role/deleted employee denial in both storage modes. [CI #40991436945](https://github.com/danwiz/project0-cardealership/actions/runs/40991436945): 341 tests per JDK. |
| SO-09 | `src/test/java/com/revature/service/AuthorizedPurchaseReviewServiceTest.java` | `89b707faeaf6f14a48a56b3509a61685d06325ff` | **Archive 11 cases; modern JDBC transaction regressions CI-covered** | Reviewer revocation, correct pending buyer, foreign-key rejection before orphan creation, ownership preservation on rollback, invalid payment terms and single-winner stock are mapped into `JdbcPurchaseBehaviorParityTest` and existing JDBC/PG16 tests. [CI #40995418505](https://github.com/danwiz/project0-cardealership/actions/runs/40995418505): 346 tests per JDK; **different implementation semantics**, not a literal transplant. |

**Decision status for all nine:** **PROPOSED / OWNER REVIEW PENDING**. Their content is retrievable at the frozen short source SHA; copying source files only after an approved redesign decision. The separately documented **15 true short-branch `git merge-tree` conflicts** remain unresolved. See [confirmed conflict register](CAR-DEALERSHIP-CONFIRMED-MERGE-TREE-REHEARSAL-2026-10-30.md) and [22-behavior test mapping](CAR-DEALERSHIP-SHORT-BRANCH-BEHAVIORAL-PARITY-2026-10-29.md).

## 2. The one auto-merged master test introduces tag-case drift

Path: `src/test/java/com/revature/service/UserLoginServiceCharacterizationTest.java`.

| Exact source | Blob | Findings |
| --- | --- | --- |
| Original common ancestor | `f93f737b797eb43288989aa52084bb015584832f` | Uppercase `@Tag("SECURITY")` / `@Tag("TARGET-BEHAVIOR")`, but old test expects direct `removeUser` to succeed |
| Protected `master` | `9a9409a5744eac5b031d3c4de1b24f62b9881dfe` | Changes two relevant tag annotations to **lowercase** `security` and `target-behavior` yet retains the historical permissive deletion expectation |
| Frozen candidate | `e7074cf0ca4db2fab3a434dce0f8ec96c19da537` | Retains uppercase security/target tags and replaces permissive deletion with `unauthenticatedDeletionFailsClosed`, requiring `SecurityException` and preserved account access |

The first successful disposable `master` integration [run #41002545989](https://github.com/danwiz/project0-cardealership/actions/runs/41002545989) automatically merged the deletion fix with the **lowercase tag** change; **346 tests passed** per Java 11 and 17, but the two differently cased annotations can affect JUnit tag-filtered security jobs. This is a **test-selection and CI governance defect**, not evidence that account deletion became permissive. The old permissive test did not return.

**Proposed explicit seventh-file disposition:** Keep the exact **candidate blob** `e7074cf0ca4db2fab3a434dce0f8ec96c19da537` in the future merged tree, preserving uppercase tags and fail-closed deletion. This should not modify historical `master`; archive its original blob and note its differing labels. An isolated CI-only merge workflow was updated to restore the candidate file and enforce the `@Tag("SECURITY")`/safe-deletion method. **Do not mark that updated workflow passed until the newest exact-head Java11/17 jobs finish.**

## 3. Explicit non-acceptance and next gates

- **Do not merge short #84 as a Git parent** just to close open draft PRs: doing so would import competing mutable Offer service and test APIs, require 15 reviewed conflicts and potentially reintroduce authorization bypasses.
- **Do not use historical `docs/PURCHASE-INTEGRITY-REVIEW.md` as a production guarantee**: it explicitly documents non-ACID behavior, limited compensation and public direct-mutation bypass.
- **Do not count CI parity as full feature equivalence**: the modern database's foreign key prevents orphan requests earlier than the historical in-memory test, and ownership now has durable IDs/contract links. Product owner must approve deliberate semantic changes.
- **Do not grant public operational admin bootstrap**: the modern operator-only design has synthetic tests but needs independent production role, password/secret channel, audit and rollback authorization.
- **Do not discard original source and tests**. Preserve original blob hashes and recoverable refs, perform independent Git bundle restore verification, then owner-sign individual dispositions.
- **Do not approve release.** The 17-gate register retains 12 promotion blockers, including actual Git source approval, canonical Maven destination, database failover/issuer-writer boundaries and independent security/DBA/QA review.

**Outcome of this document:** all nine short-only source paths have a traceable historical identifier and a proposed architectural disposition. **No short-branch merge, new production code, default-branch change or release has been authorized by documenting them.**
