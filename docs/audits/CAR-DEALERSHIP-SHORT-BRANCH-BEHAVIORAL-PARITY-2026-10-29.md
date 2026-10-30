# Car Dealership — short-branch behavioral parity register

**Date:** 2026-10-29 ET  
**Status:** DRAFT, manual source-review crosswalk; **not proof of executable equivalence**.  
**Integration:** [#85](https://github.com/danwiz/project0-cardealership/issues/85) and [canonical ADR](ADR-CAR-DEALERSHIP-CANONICAL-REPOSITORY-2026-10-29.md).  
**Short source:** `fix/atomic-account-create-20261029`, draft #84, SHA `086fbf91294f74fe4bd967256498ef94e92c501a`.  
**Long integration:** `security/integration-candidate-master-pbkdf2-parity-20261029`; latest tested prior to this review `eadc05748a1c0481d16bf97f3edeebc086170d94`.

## Purpose

The four competing short-branch PRs (#78, #82, #83, #84) include three **short-only** JUnit files, totaling **22 test methods** (six facade-role authorization, five inventory management, eleven purchase review). Copying the entire short branch would reintroduce an independent legacy console/Offer service and best-effort compensation instead of the JDBC transactional purchase architecture. The preferred action is **transfer behavior and provenance only** into current commands and interfaces.

Statuses:
- **Mapped**: same core invariant appears in a named long-side test; APIs/storage may differ, so still needs final exact-head review.
- **Partial**: nearby invariant has coverage but a precise caller, failure placement or affected data projection is not yet verified.
- **Gap**: an equivalent direct regression has not been identified in inspected long-side tests.

## Short facade/authorization tests — 6

| ID | Original short-side method in `CarDealershipRoleRevalidationTest` | Long-side evidence | Classification / action |
| --- | --- | --- | --- |
| R-01 | `rejectsMissingAccountAndNullPermission` | `RoleAuthorizationServiceTest.missingIdentityDataIsDeniedSafely` | **Mapped** — preserve null actor/permission negative cases |
| R-02 | `rejectsCallerSuppliedAdministratorRoleWithoutPersistedIdentity` | `RoleEscalationRegressionTest.applicationAndAdapterRefuseInjectedAdminRole` | **Mapped** — forged `User` not a session |
| R-03 | `revocationRejectsPreviouslyAuthorizedAdministrator` | `SessionRevocationEpochRegressionTest` and `SnapshotAuthorizationBoundaryTest` | **Mapped** — durable role/session revision required |
| R-04 | `deletedAccountCannotReusePrivilegedSessionObject` | `SessionRevocationEpochRegressionTest` | **Mapped** — deleting/recreating same identity cannot revive session |
| R-05 | `directPersistenceCallsRequireAdministratorAuthorization` | `SnapshotAuthorizationBoundaryTest.directCommandsAndAdapterFailClosedBeforeAnyStorageIO` | **Mapped** — no-actor/forged/customer calls denied |
| R-06 | `rejectsMissingUsername` | `RoleAuthorizationServiceTest.missingIdentityDataIsDeniedSafely` | **Mapped** — blank/missing identity denied |

## Short inventory tests — 5

| ID | Original method in `AuthorizedInventoryServiceTest` | Long-side evidence | Classification / action |
| --- | --- | --- | --- |
| I-01 | `authenticatedEmployeeCanAddVehicle` | `SessionDemotionInventoryRegressionTest` | **Mapped** — genuine verified employee adds a listing |
| I-02 | `customerCannotModifyInventory` | `ApplicationCommandTest.inventoryCommandRejectsUnauthorizedActors` | **Partial** — existing test denies unverified customer; add *authenticated* customer direct-command coverage in both configured storage modes |
| I-03 | `forgedRoleAndInvalidPasswordCannotModifyInventory` | `RoleEscalationRegressionTest`, verified context login and inventory command checks | **Partial** — test explicit forged customer/admin and incorrect password against configured command |
| I-04 | `revokedEmployeeCannotModifyInventory` | `SessionRevocationEpochRegressionTest` (deleted account) and `SessionDemotionInventoryRegressionTest` (role changed) | **Partial** — add direct inventory-mutation rejection after account deletion, with no DB writes |
| I-05 | `demotedEmployeeCannotModifyInventory` | `SessionDemotionInventoryRegressionTest` (in-memory and JDBC/H2) | **Mapped** — same verified actor denied post-demotion |

## Short purchase review tests — 11

| ID | Original method in `AuthorizedPurchaseReviewServiceTest` | Long-side evidence | Classification / action |
| --- | --- | --- | --- |
| P-01 | `customerCannotApproveOrRejectRequestsEvenWithForgedRole` | `JdbcPurchaseApprovalServiceTest.rejectsUnprivilegedDeletedOrForgedReviewersAndWrongCustomerRole`; `RoleEscalationRegressionTest` | **Mapped for JDBC**; check rejection command separately |
| P-02 | `revokedEmployeeCannotReviewRequests` | `JdbcReviewerRevocationRaceTest`, `SessionRevocationEpochRegressionTest` | **Partial** — explicit deleted reviewer failure during request review still to crosswalk on a final integrated SHA |
| P-03 | `pendingBuyerLookupRequiresReviewerAndReturnsRequester` | `JdbcInventoryRepositoryTest`, `ApplicationCommandTest` | **Partial** — confirm buyer projection and unauthorized lookup through configured query boundary |
| P-04 | `missingBuyerCannotConsumeInventoryOrPendingRequest` | `JdbcPurchaseApprovalService` locked buyer/role SQL checks; `PostgresqlPurchaseApprovalIntegrationTest` | **Partial** — add exact non-existent persisted buyer case with no stock/ownership/plan writes |
| P-05 | `purchaseApprovalAssignsRegisteredBuyerAndConsumesInventoryOnce` | `JdbcPurchaseApprovalServiceTest.approvedPurchaseCommitsAllFourRowsAndReplaysIdempotentlyAcrossInstances` | **Mapped for JDBC** — stable contract and single durable buyer ownership |
| P-06 | `soldOutApprovalLeavesBuyerOwnershipUnchanged` | `JdbcPurchaseApprovalServiceTest.twoBuyersCannotConsumeOneVehicleWithSeparateJdbcConnections` | **Mapped for JDBC** — single winner, no double sale |
| P-07 | `mutationThenExceptionRestoresStockRequestAndOwnership` | `JdbcPurchaseApprovalServiceTest.everyInjectedWriteFailureRollsBackTheEntirePurchase` | **Mapped for JDBC ACID**, not equivalent to old `Offer` compensation |
| P-08 | `inventoryCommitFailureRemovesOnlyStagedOwnership` | `JdbcPurchaseApprovalServiceTest.everyInjectedWriteFailureRollsBackTheEntirePurchase` | **Partial** — JDBC transactional rollback superior for durable records; existing unrelated buyer ownership still requires a focused negative assertion |
| P-09 | `ownershipWriteFailureDoesNotConsumeInventoryOrPendingRequest` | `JdbcPurchaseApprovalServiceTest.everyInjectedWriteFailureRollsBackTheEntirePurchase`; PostgreSQL ownership-insert rollback | **Mapped for JDBC** |
| P-10 | `concurrentApprovalsCannotSellOneVehicleTwice` | `JdbcPurchaseApprovalServiceTest.twoBuyersCannotConsumeOneVehicleWithSeparateJdbcConnections`; `PostgresqlPurchaseApprovalIntegrationTest` | **Mapped for JDBC/PG16** |
| P-11 | `authorizedEmployeeReceivesInputValidation` | `JdbcInventoryRepositoryTest.unknownIdentifiersAndInvalidTermsAreRejected` and approval validations | **Partial** — ensure negative and overflow payment terms are rejected by actual review command |

## Explicit next steps

1. **Add tests for I-02/I-03/I-04** on the isolated integration branch (two configured modes), using actual authenticated actors and a trusted fixture writer, without copying `AuthorizedInventoryService`.
2. Add a focused P-04 test for missing persisted buyer; assert request remains PENDING, stock unchanged, ownership/plan count zero on actual JDBC transaction.
3. Review P-03 and P-08 with a domain owner to decide whether equivalent buyer projection and previously committed ownership isolation are required in the modern portfolio product, rather than silently removing historical behavior.
4. Verify the *full integrated candidate SHA*, not the short branch alone, on Java 11/17 and PostgreSQL 16. Only then reclassify mapped/partial/gap to accepted/declined in issue #85.
5. Keep short source files and original logs immutable. Do not cherry-pick best-effort purchase compensation into the JDBC transactional service. No default-branch or Maven-target promotion without signed architecture decision.

**This register is review evidence, not a claim that all 22 behavioral tests have been transferred or that either branch is production-ready.**


## Implementation checkpoint — 2026-10-29 ET

A focused test-only parity transfer was committed on the **isolated integration candidate**, not the original short branch:
- `src/test/java/com/revature/service/SessionDemotionInventoryRegressionTest.java`: added `customerForgeryAndDeletedEmployeeCannotMutateInventoryInMemory` and `customerForgeryAndDeletedEmployeeCannotMutateInventoryJdbc`, extending the existing two demotion tests.
- For both configured storage modes, an incorrect staff password is rejected, an **actually authenticated customer** cannot add/remove inventory, a **copied username/role/password hash/session revision** cannot forge an administrator session, a legitimate staff member can add inventory, and **deleting** that employee then prevents further add/remove mutation without altering listing count.
- These tests directly address the earlier **I-02/I-03/I-04 partial gaps**. They are not copies of `AuthorizedInventoryService`; they use the real `ManageInventoryCommand` and `ConfiguredDomainAdapter`.
- Exact branch head at implementation `e4a24a588c8faa92cabb6f4ec0c7ca1b463550a3`. [Java 11/17 CI #40991436945](https://github.com/danwiz/project0-cardealership/actions/runs/40991436945) was **queued at this checkpoint**; classify I-02/I-03/I-04 as **IMPLEMENTED, AWAITING CI** until exact-head logs confirm.

The earlier application-session bridge (separate opt-in legacy credential upgrade followed by normal context-bound login) passed [CI #40991023039](https://github.com/danwiz/project0-cardealership/actions/runs/40991023039), exact head `768e9998b7ea9477ebfa8a8fe22d2699a98b3c91`: **339 tests on both Java 11 and Java 17**, zero failures/errors/skips, including two non-skipped `LegacyCredentialApplicationSessionIntegrationTest` cases.

The 11 short-only purchase-review tests require a separate signed-off crosswalk for P-02/P-03/P-04/P-08/P-11. The old best-effort in-memory compensation algorithm is not approved for transplant into the JDBC transaction writer. No PR merge, default-branch change, production SQL, credential migration or release.

## Exact-head verification — short inventory tests (2026-10-29 ET)

**Verified:** [GitHub Actions #40991436945](https://github.com/danwiz/project0-cardealership/actions/runs/40991436945) completed **SUCCESS** at isolated candidate SHA `e4a24a588c8faa92cabb6f4ec0c7ca1b463550a3`. Java **11 and 17 each passed 341 tests, zero failures/errors/skips**, with Maven test and package verify BUILD SUCCESS. Both job logs show **4 non-skipped `SessionDemotionInventoryRegressionTest` cases** (including both new storage-mode tests for authenticated customers, forged administrator actor, wrong-password login, revoked/deleted employee) and **2 `LegacyCredentialApplicationSessionIntegrationTest` cases**.

**Disposition update:** I-02/I-03/I-04 now **COVERED IN ISOLATED CANDIDATE AND CI-VERIFIED**, rather than awaiting test verification. They still need final integrated SHA review, short/long repository decision and independent security acceptance. P-02/P-03/P-04/P-08/P-11 remain partial pending precise test or owner-approved scope decision. This does not justify merging either competing leaf.


## Phase 9 — five JDBC purchase-behavior regressions (2026-10-29 ET)

To close the remaining short-only purchase review evidence without importing the best-effort `AuthorizedPurchaseReviewService`, five JUnit cases were added as `src/test/java/com/revature/repository/jdbc/JdbcPurchaseBehaviorParityTest.java` to the **existing isolated integration candidate**, commit `6b332471f8deb6e7308a18c9960c00141b860bf2`.

| Short parity | New direct scenario | Initial status |
| --- | --- | --- |
| P-02 | Deleted/revoked verified reviewer cannot approve or inspect pending requests, with unchanged purchase/stock/ownership | IMPLEMENTED — CI pending |
| P-03 | Authenticated reviewer sees exact persisted pending customer; authenticated customer denied access; immutable view | IMPLEMENTED — CI pending |
| P-04 | Unknown buyer is rejected at **purchase_requests.customer_name FK insert**, before an orphan request exists; no stock/ownership/payment change | IMPLEMENTED — CI pending (structurally different from the legacy late approval check) |
| P-08 | Separate earlier committed ownership and payment plan survive a later purchase failure injected after new ownership insertion; rollback preserves original data | IMPLEMENTED — CI pending |
| P-11 | Authorized reviewer and direct JDBC service reject zero/negative terms and negative request identifier without changing any row | IMPLEMENTED — CI pending |

The tests use a disposable per-case H2 database in PostgreSQL mode, a genuine context-bound verified reviewer, and the real `JdbcPurchaseApprovalService`, `JdbcInventoryRepository`, `DealershipQueryService` and `ReviewPurchaseRequestCommand`. They do **not** prove physical PostgreSQL failover, real production principals, or equivalence of the original in-memory compensation algorithm. [Java 11/17 CI #40995418505](https://github.com/danwiz/project0-cardealership/actions/runs/40995418505) was **in progress** when the evidence register was updated. Leave dispositions pending until exact-head logs show all five tests executed, 0 skipped/failures.

**No default-branch merge, competing short-branch edit, new pull request, production access, release, or deployed migration.**

## Phase 9 exact-head purchase parity CI acceptance — 2026-10-29 ET

**VERIFIED:** [GitHub Actions #40995418505](https://github.com/danwiz/project0-cardealership/actions/runs/40995418505) **COMPLETED SUCCESS** on immutable isolated integration candidate `6b332471f8deb6e7308a18c9960c00141b860bf2`. Both actual job logs show **`JdbcPurchaseBehaviorParityTest`: 5 executed, 0 failures/errors/skips** in Maven test and package verification on **Java 11 and Java 17**. Both total **346 tests/job, 0 failures/errors/skips**, with `BUILD SUCCESS`.

**P-02, P-03, P-04, P-08, P-11 are now CI-COVERED in the isolated modern JDBC/H2 candidate**:
- P-02: persisted reviewer removed; approval and pending-buyer disclosure denied, with zero purchase mutation.
- P-03: authenticated reviewer sees exact immutable pending requester, customer denied.
- P-04: unknown buyer rejected at FK-constrained *request insertion*, preserving all state. The legacy approach allowed creating an orphan then rejecting at approval; this is intentionally replaced with stronger earlier validation, **not** reproduced literally.
- P-08: a later failed purchase at `AFTER_OWNERSHIP` rolls back without erasing an earlier committed ownership and payment plan.
- P-11: negative/zero payment terms and invalid negative request ID denied at both command/service boundaries.

**Qualification:** This closes the identified *test coverage* gaps on this isolated candidate. It is **not** a full executable equivalence certification of the short branch or a production acceptance. PostgreSQL16 independent issue #89 fault/recovery and permit/receipt CI evidence remains separately gated; these new five cases use H2 in PostgreSQL compatibility mode. Canonical repo/branch integration and owner/security signoff remain NO-GO.
