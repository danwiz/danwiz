# ADR (Proposed): Car Dealership repository authority, provenance, and integration path

- **Date:** 2026-10-29 ET (evidence validated on live GitHub)
- **Status:** PROPOSED — owner decision and independent review pending. **Not a migration or merge authorization.**
- **Owner:** `danwiz`; related [issue #85](https://github.com/danwiz/project0-cardealership/issues/85), [issue #25](https://github.com/danwiz/project0-cardealership/issues/25), [portfolio audit PR #25](https://github.com/danwiz/danwiz/pull/25)
- **Scope:** `danwiz/project0-cardealership` (preservation and active Java 11/17/JDBC security stack) and `danwiz/Project0-Cardealership-Maven` (Java 17 Maven target and portfolio README)

## 1. Decision needed

**Which repository is the canonical future product, and how do we preserve original training artifacts?**

The `Project0-Cardealership-Maven` README **explicitly calls that repository the authoritative modernization target**, stating that its initial training implementation is preserved and remains not production-ready or pin-ready. That is a *documented project intention*, not proof that the active engineering work currently lives there.

Conversely, `project0-cardealership` contains the **91 open draft PRs** and all the current Java 11/17, JDBC/PostgreSQL 16, authorization, purchase-integrity, recovery, and security design proofs. Its `master` and latest development head lack a top-level README; the root contains original Eclipse metadata (`.classpath`, `.project`, `bin/`) and a `BUILDING.md`. The separately named Maven repo also contains `target/` and Eclipse metadata. No cleanup or rename is authorized by this ADR.

It would be misleading to say the modern Java 11/17/JDBC code has already migrated into the repository whose README declares it canonical.

## 2. Alternatives

| Option | Description | Advantages | Material risks |
| --- | --- | --- | --- |
| A — Keep Maven repo as canonical future *portfolio application* | Preserve `project0-cardealership` as source/evidence and integration workspace, port an accepted, versioned subset into `Project0-Cardealership-Maven` after testing | Honors existing README and clean separation between source heritage and published application | Large controlled import; provenance, history and license reconciliation; branch drift; destination's Java 17/legacy serialization differs from Java 11/17/JDBC stack |
| B — Promote `project0-cardealership` itself | Once accepted, modernize main branch; point Maven repo at its origin/archive | Preserves active PR history with fewer cross-repo moves | Changes current repository's historical role; `master` security/characterization drift; 91-PR integration and cleanup |
| C — Maintain two independently evolving products | Publish both as active | Can support two pedagogical approaches | Duplicate ownership, confusion, security drift, double maintenance; **not recommended** without sharply distinct requirements |

## 3. Proposed decision for maintainer approval

**Provisional preference: Option A**, consistent with the Maven repository's own authoritative-target declaration:
1. `danwiz/project0-cardealership`: **preserved academic origin + technical modernization staging/evidence**. Preserve full Git history, original Java and Eclipse source, releases/tags, original attribution and license evidence, and active issue traceability. Avoid force-pushes.
2. `danwiz/Project0-Cardealership-Maven`: **candidate canonical portfolio application**, not yet accepted. Do not import, rename, delete or publish until the maintainers approve exact release scope, Java support policy and persistent-data migration. A future product rename is a separate ADR.
3. `danwiz/danwiz`: **portfolio gateway and audit evidence**, linking the canonical product and explaining the historical implementation.

A maintainer can instead select Option B, but must record the choice, rationale, aliases/redirects, original provenance and test impact **before code moves**.

## 4. Current verified branch geometry

- `project0-cardealership/master` is the published default baseline.
- Bottom PRs: **#5 -> #6**. From #6, the **long chain starts #7** and the competing **short chain starts #78**. Independent documentation root **#46** targets `master`.
- Exact count **91 open/draft PRs**: **2 shared (#5/#6) + 84 long-chain (#7 through #104 with actual open numbers only) + 4 short-chain (#78/#82/#83/#84) + 1 independent #46**.
- Latest long leaf **#104**: `45eccdc73ce36d4298326498a3603e2363251fd6`; latest short leaf **#84**: `086fbf91294f74fe4bd967256498ef94e92c501a`. Both remain drafts/unmerged.
- Short/long merge base: `ad8d03574c7f048b236c9d24f0c03ac54dffcbd7`; long is **341 ahead / 109 behind** the short.
- Latest long/master merge base: `9c242f9880a18a7749621a6ed5f6d53d3ee5fcdc`; long **356 ahead / 16 behind** `master`. These are *exclusive commit counts*, not PR or conflict counts.
- Exact changed-path intersection long vs short: **16 paths**; short comparison has **9 additional paths** not in the long path list. Compared against long, `master` has **9 changed paths** carrying 16 unique commits.

## 5. Non-negotiable protection against default-branch regression

The `master` `Pbkdf2PasswordHasher` is materially stronger than the latest long branch:
- `master`: **600,000** PBKDF2-HMAC-SHA256 default iterations, **2,000,000** hard verification cap, **512-character** maximum encoding, 16-byte salt and fixed 256-bit derived-key-length validation, with regression tests for invalid work factors.
- Long draft #104: **120,000** default iterations, no explicit maximum work factor/encoded length, constructor accepts any positive work factor/key length, and verification derives output length from a *stored untrusted* hash. Those changes can create a **work-factor / parser resource-exhaustion risk** and reduce new password hashing strength if blindly adopted.
- OWASP Password Storage Cheat Sheet currently recommends **PBKDF2-HMAC-SHA256 ≥600,000** iterations when PBKDF2 is selected for FIPS environments: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- **Do not replace `master` PBKDF2 semantics with the long branch's version.** New writes must meet approved modern policy. Existing 120k hashes need an explicit **bounded verification + rehash-on-login/forced rotation migration policy**, not a sudden silent lockout. Performance and compatibility require benchmarks/review.
- Bring the master-only `rejectsUntrustedWorkFactorsBeforeHashing` test forward (or equivalent), plus length/salt/hash-length and low/high iteration tests. Tests must fail closed for forged or massive work factors before doing PBKDF2.

## 6. Required decision and stage gates

1. **DECIDE** authority (Option A/B), product name/version and whether modernization is a portfolio demonstration or intended production service.
2. **PRESERVE** immutable original evidence: artifact register, branch/tag SHAs, files/hashes, academic provenance, third-party dependency/license inventory.
3. **RECONCILE** all nine `master`-side changed paths, all 16 cross-branch overlaps and the nine short-only candidates in a separately reviewed file-level disposition register.
4. **STAGE** a single ephemeral integration candidate, distinct from `master` and distinct from both existing draft leaves; no force-push. Import only approved behavior and explicitly compare SQL, identity, console and file-persistence contracts.
5. **TEST** exact candidate on Java 11 and 17, disposable PostgreSQL 16 migrations/permissions/revocation, security test parity, actual pre/post COMMIT transport cuts, signed artifacts/SBOM/license verification, and reproducible build. Clean tests on the old leaf do **not** validate the integrated candidate.
6. **REVIEW** using independent code/security/DBA reviewers. Establish rollback, release owner and production-no-go evidence.
7. **PROMOTE** only with explicit owner approval, a release tag and README/portfolio traceability. Until then, classify both as development/testing; neither is production.

## 7. Decision log

| Field | Status |
| --- | --- |
| Preferred option | A — retain Maven repo as **provisional** canonical target |
| Owner approval | **Pending** |
| Cross-repository code movement | **Not performed** |
| Default-branch merge or branch retarget | **Not performed** |
| Production migration / release | **Not performed** |
| Current risk decision | **NO-GO** |

*This ADR states a proposed governance decision and records evidence. It must not be interpreted as implementing Option A without approval.*
