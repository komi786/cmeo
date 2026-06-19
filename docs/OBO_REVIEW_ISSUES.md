# CMEO — OBO Foundry Review: Action Items

Reviewer release reviewed: **2025-12-10** (`owl:versionIRI .../releases/2025-12-10/cmeo.owl`, `versionInfo 1.0.2`).
File under review: [`cmeo.owl`](../cmeo.owl) (8,821 lines, 70 native `CMEO_*` classes).

This is the reviewer's feedback restructured into discrete, independently-fixable tasks, grounded against the
current ontology. Each item lists **what / where / fix**. Work top-to-bottom: the **Blocking (MUST)** section first.

Legend: 🔴 MUST (blocking) · 🟠 SHOULD · 🟡 RECOMMEND/NICE-TO-HAVE.

---

## A. Malformed / non-conformant IRIs — 🔴 MUST

These violate the [OBO identifier scheme](http://obofoundry.org/id-policy). Every native term must be
`http://purl.obolibrary.org/obo/CMEO_NNNNNNN` (http, underscore, zero-padded number — no `.owl`, no `#fragment`, no word IRIs).

- [ ] **A1. `cmeo.owlduration_of_observation`** — IRI is `http://purl.obolibrary.org/obo/cmeo.owlduration_of_observation` (cmeo.owl:8151). Mint a proper `CMEO_00000NN` IRI and update all references (subClassOf of `IAO_0000416`). Label "duration of observation".
- [ ] **A2. `cmeo.owl#code_set`** — uses a `#fragment` IRI (cmeo.owl:8162) and is also referenced as a parent at cmeo.owl:3470 and cmeo.owl:3486. **Note:** this block already carries `oboInOwl:id → IAO_0020020` and the IAO definition → it is really IAO's *code set*. **Fix = reuse the IAO IRI `http://purl.obolibrary.org/obo/IAO_0020020` directly** (drop the CMEO fragment class) and repoint the two child references. See also **D1** (children are mis-placed under it).
- [ ] **A3. `cmeo.owl#composite_endpoint_specification`** — uses a `#fragment` IRI (cmeo.owl:8174). Mint a proper `CMEO_00000NN` IRI (it subclasses `CMEO_0000063`) and update references.

> After fixing, grep to confirm zero matches: `grep -n 'cmeo\.owl[#a-z]' cmeo.owl` should return nothing.

---

## B. Term duplication / re-minted IRIs — 🔴 MUST

These are labelled/defined as imports from another OBO ontology but mint a **new** `CMEO_*` IRI instead of reusing the
source IRI. Reuse the original IRI (preferred), **or** justify that the meaning genuinely differs and re-scope the label/definition.

- [ ] **B1. `CMEO_0000008` "formula"** (cmeo.owl:3302) — claims ChEBI origin but the definition ("an ICE that specifies a mathematical/logical expression…") is *not* ChEBI's usage, and the ChEBI IRI is malformed. Decision: this is not the ChEBI concept → **re-scope with a more specific label** (e.g. "derived-value formula" / "computation formula specification") and drop the ChEBI provenance, OR reuse an existing ICE/STATO term if one matches.
- [ ] **B2. `CMEO_0000013` "adverse event"** (cmeo.owl:3376) — stated as from OAE but re-minted **and undefined**. Reuse `OAE:0000001` (adverse event) instead of a CMEO IRI.
- [ ] **B3. `CMEO_0000014` "adverse drug event"** (cmeo.owl:3387) — same problem as B2; reuse the OAE term.
- [ ] **B4. `CMEO_0000036` "consumption measurement"** (cmeo.owl:3621) — copied from CMO *including the definition*. **Reuse the original CMO IRI**; remove the CMEO mint.
- [ ] **B5. `CMEO_0000060` "categorical variable"** (cmeo.owl:3889) — from STATO and **undefined** in CMEO. Reuse `STATO_0000060`.

### Object properties (also re-minted) — 🔴 MUST
- [ ] **B6. `is in mapping relation with` + children** (label at cmeo.owl:2513) and **`is related to` + children** (cmeo.owl:2523). These are stated as from SIO/SKOS but mint new IRIs and carry no real definitions; they also exist in MCRO. Since **none appear to be used in any axiom**, the simplest fix is to **remove them**. (Alternative: reuse the existing SIO/SKOS/MCRO IRIs.) Confirm non-use before deleting: `grep -n 'is in mapping relation\|is related to' cmeo.owl`.

---

## C. New-term scope — terms that belong in another OBO ontology — 🟠 SHOULD

Obligation is to *attempt* submission upstream; a rejection means the term stays. File the upstream tracker issues, link them here.

- [ ] **C1. `CMEO_0000068` "healthy volunteer criterion"** (cmeo.owl, term scan) → submit to **OBI**. Reviewer also suggests it should be a child of `OBI:0002453` "health status inclusion criterion" (see D-hierarchy).
- [ ] **C2. `CMEO_0000073` "exploratory data analysis"** → submit to **OBI**.
- [ ] **C3. Other children under "exclusion criteria"** → submit to **OBI**. Enumerate them and list each as a sub-checkbox.
- [ ] **C4. `CMEO_0000002` "wearable device"** → likely **OBI** (see also F1, definition rewrite).
- [ ] **C5. `CMEO_0000003` "sensor"** → out of scope as-is; either import from elsewhere or submit a narrowly-scoped label to **OBI** (see F2).

**Stays in CMEO (reviewer agreed — no action, just don't move them):** `CMEO_0000029` "OMOP identifier" (IAO doesn't enumerate identifiers); `CMEO_0000004` "medical encounter" (adaptation of an NCIt term).

---

## D. New-term hierarchy placement — 🟠 SHOULD

- [ ] **D1. `code_set` children** — `code_set` (A2) is defined like a whole identifying *system/registry*, but is used as the **parent of individual identifiers** (e.g. centrally registered identifier). Repoint those children to the correct parent, or add a usage example justifying the placement. (Resolved together with A2.)
- [ ] **D2. "observation" hierarchy mixes observations with events** — terms under `observation` are a mix of observations and events that can occur without observation. Decide the priority per term: if the **event** is primary → move it elsewhere in the hierarchy; if the **record** is primary → rename to reflect that (e.g. "… observation"/"… record"). Affects `CMEO_0000010` "clinical event" (see F4).
- [ ] **D3. "plan specification" children are parts, not whole plans** — new CMEO terms under `plan specification` look like *parts* of plan specifications. Review and either re-parent under a "part of plan specification" grouping or correct the relation.

---

## E. Imported-term correctness — 🟠 SHOULD

### E1. Imported under the wrong label — update labels to the source's primary label
- [ ] **E1a. `IAO_0000100`** — CMEO label "dataset" (cmeo.owl:4882; note also `IAO_0000111 "data set"` at :4870). Primary IAO label is **"data set"** ("dataset" is a synonym). Use the primary label; keep CMEO usage as synonym only.
- [ ] **E1b. `IAO_0000027`** — CMEO label "data item" (synonyms incl. "data matrix"). Primary IAO label is **"data entity"** ("data item" is a synonym). Update.
- [ ] **E1c. `OBI_0300311`** — CMEO label "observational design". Primary OBI label is **"observation design"**. Update.

### E2. Imported under the wrong parent — restore native hierarchy
- [ ] **E2a. `STATO_0000142` "correlation coefficient"** — natively `statistic (STATO_0000039) → correlation coefficient`. In CMEO it sits under `OBCS_0000218 "derived data from statistical analysis"` (and `STATO_0000039` is also imported). Restore the native parent.
- [ ] **E2b. `OBCS_0000068` "frequency distribution"** — placed under the **undefined** `STATO_0000225 "probability distribution"`; move it under the **defined** `OBCS_0000010 "probability distribution"` (preserves native hierarchy, keeps a defined parent).

### E3. Wrong term selected — pick the canonical term
- [ ] **E3a. `SIO_000027` "process quality"** used inside an otherwise all-PATO branch (cmeo.owl:~8186). PATO already has "process quality" with an equivalent definition → replace with the PATO term.
- [ ] **E3b. `OBI_0100026` "organism"** is **deprecated** (referenced at cmeo.owl:5277). Replace with **`COB_0000022` "organism"**.

### E4. Import hygiene — 🟡 RECOMMEND
- [ ] **E4a. Multiple definitions/labels** — several dozen terms (mostly IAO/OBI) carry conflicting definitions/labels because they're pulled from more than one source. Import **only the terms you need, from the single primary source**, ideally via a proper import module (ROBOT extract / MIREOT) rather than hand-copied axioms.

---

## F. Specific term definition fixes — 🟡 RECOMMEND (some MUST for missing defs, see H1)

- [ ] **F1. `CMEO_0000002` "wearable device"** (cmeo.owl:3253) — definition is convoluted, copies IoT marketing text, and embeds an unattributed `[5]` reference. Rewrite as a clean genus–differentia definition; submit to OBI (C4).
- [ ] **F2. `CMEO_0000003` "sensor"** (cmeo.owl:3266) — **self-referential** ("A sensor that is worn…"). Rewrite referencing the parent; make the label more specific to the wearable scope.
- [ ] **F3. `CMEO_0000008` "formula"** — label implies something broader than defined; narrow the label (ties to B1).
- [ ] **F4. `CMEO_0000010` "clinical event"** (cmeo.owl, term scan) — definition conflates the **event** with the **recording** of the event. Separate the two (ties to D2).
- [ ] **F5. `CMEO_0000016` "device adverse event"** (term scan) — **self-referential** ("A medical device adverse event that is…"). Rewrite via parent.
- [ ] **F6. `CMEO_0000026` "code"** (cmeo.owl:3469) — ambiguous label; definition ≈ `IAO_0000578` "centrally registered identifier". **Reviewer recommends removal** (reuse IAO term where needed).
- [ ] **F7. `CMEO_0000028` "missing value specification"** (cmeo.owl:3511) — unclear definition ("It indicate the missing value indicator…"); clarify what "It" / "value indicator" mean and relate to parent `value specification`; add an example. Reviewer suggests modelling as a property value (`'missing value specification' some 'weight'`) rather than a subclass of the thing that's missing.
- [ ] **F8. `CMEO_0000033` "blood biomarker"** & **F9. `CMEO_0000034` "protein biomarker"** (cmeo.owl:3587, :3598) — out of scope and mis-placed as children of "blood measurement" (conflates measurement with what is measured); protein biomarkers especially aren't blood-specific. Re-parent (separate biomarker entity from measurement) or remove.
- [ ] **F10. `CMEO_0000059` "data type"** (cmeo.owl:3878) — **self-referential** ("data type of variables such as int, float…"). Rewrite via parent.
- [ ] **F11. `CMEO_0000074` "start time"** & **F12. `CMEO_0000075` "end time"** (cmeo.owl:4037, :4053) — both equivalently/under-defined as `'has value' some xsd:dateTime`, making them identical to any `owl:Thing` using dateTime. Give each a proper differentiating definition (or remove if redundant with an existing temporal term).
- [ ] **F13. `CMEO_0000076` "category"** (cmeo.owl:4069) — over-generic grouping term that hides useful terms and has few children; reviewer recommends **removal**.
- [ ] **F14. `CMEO_0000079` "data access"** (cmeo.owl:4146) — definition is actually "*authorized* data access"; either broaden the definition to match the label or narrow the label.
- [ ] **F15. `code_set` usage** — add a usage example or delete (ties to A2/D1).
- [ ] **F16. Over-broad labels (general)** — audit labels that imply more than the definition covers; scope each label precisely.

---

## G. Naming conventions — 🟠 SHOULD

- [ ] **G1. No plurals:** `CMEO_0000039` "stages and scales", `CMEO_0000043` "medications and therapies", `CMEO_0000046` "demographics" (also ambiguous singular vs plural — review meaning). Rename to singular.
- [ ] **G2. No compound ("and"/"or") names:** `CMEO_0000039` "stages and scales", `CMEO_0000043` "medications and therapies", `CMEO_0000045` "compliance or adherence", `CMEO_0000048` "lifestyle and behavior". Split into separate terms or pick a single genus label.

---

## H. Recurrent / housekeeping — 🟠 SHOULD

- [ ] **H1. Missing definitions** — reviewer counts ~12/70 undefined (~17%). Confirmed undefined in this build: `CMEO_0000004`, `CMEO_0000013`, `CMEO_0000014`, `CMEO_0000060`, `CMEO_0000074`, `CMEO_0000075` (others may surface — re-run the scan). Supply `IAO_0000115` definitions for all native terms. *(Note: 13/14/60 also resolve via reuse in B2/B3/B5; 04 stays per C.)*
- [ ] **H2. Apostrophes / non-text characters** — reviewer saw mojibake like `patientâ€™s`. Current build shows **0 matches** for `â€` — likely already fixed in 1.0.2; verify across all annotation text before release and normalize curly→straight quotes consistently.
- [ ] **H3. Self-referential definitions** — covered individually: F2 (sensor), F5 (device adverse event), F10 (data type). Redefine each by referencing its parent.

---

## Suggested order of work

1. **A** (malformed IRIs) → **B** (re-minted IRIs / object properties) — these are the hard blockers and several resolve other items (B2/B3/B5 also clear H1 entries; A2 clears D1).
2. **E** (imported-term labels, parents, deprecated `OBI_0100026`→`COB_0000022`) — mechanical, high-confidence.
3. **H1** remaining missing definitions + **H3** self-referential rewrites.
4. **G** naming (plurals/compounds) — touch labels once.
5. **C** upstream submissions (OBI etc.) — file trackers, can run in parallel; rejection = stays.
6. **D / F** hierarchy + definition-quality passes.
7. Re-run reasoner (Protégé/ELK) + ROBOT report; bump `versionInfo` / `versionIRI`.

## Verification checklist before re-release
- [ ] `grep -n 'cmeo\.owl[#a-z]\|cmeo\.owlduration' cmeo.owl` → empty
- [ ] All `rdf:about` for native terms match `obo/CMEO_[0-9]{7}`
- [ ] ROBOT report: no missing definitions on native terms
- [ ] Reasoner runs clean (no unsatisfiable classes)
- [ ] No `OBI_0100026`; `COB_0000022` present instead
