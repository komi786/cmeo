# CMEO imports — MIREOT re-import setup

This folder regenerates CMEO's **imported terms** from their source ontologies using ROBOT's
MIREOT extraction, instead of hand-copying them into `cmeo.owl`. Doing this once clears, in a
single pass, three classes of issue the review/dashboard flagged:

- **imported-label mismatches** (e.g. `data item` vs source label) — modules carry the source's
  own label, so nothing diverges;
- **duplicated annotations** (the `multiple_definition` / `multiple_label` ROBOT errors, caused
  by inline copies with both a plain and an `xml:lang` value) — MIREOT emits one clean copy;
- **bare stubs** (imported classes with only a label + `subClassOf`, no definition/ID — the
  ~40 BFO/OBI leftovers and the DUO permission branch) — MIREOT pulls each term's real
  metadata from source.

## What's here

- `*_terms.txt` — seed lists: every external OBO IRI CMEO reuses, grouped by source ontology
  (generated from the current `cmeo.owl`; 16 sources, ~416 terms). Regenerate with
  `make_term_lists.py` if CMEO's imports change.
- `extract.sh` — runs `robot extract --method MIREOT` per source into `modules/<src>_import.owl`.
  Uses the vendored owls under `../sources/_imported/` where present (obi, iao, stato, obcs, duo)
  and downloads the rest (bfo, ro, pato, ogms, cmo, cob, oba, omo, reo, scdo, gaz) to `mirror/`.

## Run it

```bash
# one-time: install ROBOT (brew install robot, or put robot.jar's `robot` on PATH)
cd imports
bash extract.sh          # -> imports/modules/*_import.owl
```

## Assemble the release

MIREOT gives you clean import *modules*. To use them you split CMEO into an **edit file** that
owns only what CMEO mints, and let the modules supply everything else:

1. **Create `cmeo-edit.owl`** = the ontology header + the **native `CMEO_*` classes and the new
   `CMEO_0000084` 'is record of' property** + `owl:imports` for each module, e.g.
   ```xml
   <owl:Ontology rdf:about="http://purl.obolibrary.org/obo/cmeo.owl">
     <owl:imports rdf:resource="http://purl.obolibrary.org/obo/cmeo/imports/bfo_import.owl"/>
     <owl:imports rdf:resource="http://purl.obolibrary.org/obo/cmeo/imports/iao_import.owl"/>
     ... one per module ...
   </owl:Ontology>
   ```
   Delete the inline imported-term blocks from the edit file (they now come from modules).

2. **Keep the CMEO-added axioms that sit on imported/reused terms** — these are NOT in the
   source ontologies, so they must live in `cmeo-edit.owl`, asserted against the imported IRIs:
   - `OGMS:0000014` (clinical finding, reused): `is about some BFO:0000016` (disposition);
   - `STATO:0000252` (categorical variable): `has value specification some OBI:0001930`;
   - `STATO:0000251` (continuous variable): `has value specification some OBI:0001931`;
   - `STATO:0000090` (binary class variable): `subClassOf STATO:0000252` + `has value
     specification exactly 2 OBI:0001930`;
   - `STATO:0000087` (multi class variable): `has value specification min 3 OBI:0001930`;
   - `STATO:0000142` (correlation coefficient): `subClassOf STATO:0000039`;
   - `OBCS:0000068` (frequency distribution): `subClassOf OBCS:0000010`;
   - the `AllDisjointClasses` over measurement/procedure/therapeutic-intervention/clinical-finding;
   - plan-spec `part of some OBI:0500000` axioms (already on native terms — fine).

3. **Merge + reason into the release**:
   ```bash
   robot merge --input cmeo-edit.owl \
     | robot reason --reasoner hermit \
         --output cmeo.owl
   robot report --input cmeo.owl --fail-on error      # must pass
   python3 ../qc_report.py cmeo.owl                    # 0 errors
   ```

## Caveats / decisions for you

- **Labels become source-canonical.** MIREOT will set `IAO:0000027` to whatever IAO ships
  (the reviewer said that is `data entity`). If you deliberately want to keep `data item`,
  override the label in `cmeo-edit.owl` *after* import rather than editing the module.
- **Download URLs** in `extract.sh` point at the current OBO PURLs; pin to a dated release
  (`.../obo/bfo/2020/bfo.owl` etc.) if you want reproducible builds.
- **NCBITaxon / GAZ** are huge; MIREOT with a term file only pulls the listed terms, so it stays
  small — but the first download of the full source can be large. Consider `--input-iri` with a
  slim/subset product where one exists.
- This is a repo-architecture change (edit file + modules + build). It does not alter CMEO's
  semantics; it changes how the release `cmeo.owl` is produced. Commit `cmeo-edit.owl`,
  `imports/`, and the build command; treat `cmeo.owl` as a generated artifact.
