#!/usr/bin/env bash
# MIREOT import extraction for CMEO.
# Regenerates clean import modules (source-faithful labels, definitions, IDs, hierarchy)
# for every external OBO term CMEO reuses — replacing the hand-maintained inline imports
# that currently cause label mismatches, duplicated annotations, and bare stubs.
#
# Requires ROBOT on PATH (https://github.com/ontodev/robot/releases) and internet for the
# sources not already vendored under ../sources/_imported/.
#
#   cd imports && bash extract.sh
#
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p mirror modules

# source ontology -> where to get the full owl to MIREOT from.
# Local (already vendored) sources are used as-is; the rest are downloaded once to mirror/.
declare -A SRC=(
  [obi]="../sources/_imported/obi.owl"
  [iao]="../sources/_imported/iao.owl"
  [stato]="../sources/_imported/stato.owl"
  [obcs]="../sources/_imported/obcs.owl"
  [duo]="../sources/_imported/duo.owl"
  [bfo]="http://purl.obolibrary.org/obo/bfo.owl"
  [ro]="http://purl.obolibrary.org/obo/ro.owl"
  [pato]="http://purl.obolibrary.org/obo/pato.owl"
  [ogms]="http://purl.obolibrary.org/obo/ogms.owl"
  [cmo]="http://purl.obolibrary.org/obo/cmo.owl"
  [cob]="http://purl.obolibrary.org/obo/cob.owl"
  [oba]="http://purl.obolibrary.org/obo/oba.owl"
  [omo]="http://purl.obolibrary.org/obo/omo.owl"
  [reo]="http://purl.obolibrary.org/obo/reo.owl"
  [scdo]="http://purl.obolibrary.org/obo/scdo.owl"
  [gaz]="http://purl.obolibrary.org/obo/gaz.owl"
)

for src in "${!SRC[@]}"; do
  terms="${src}_terms.txt"
  [[ -f "$terms" ]] || { echo "skip $src (no $terms)"; continue; }
  loc="${SRC[$src]}"
  if [[ "$loc" == http* ]]; then
    owl="mirror/${src}.owl"
    [[ -f "$owl" ]] || { echo "downloading $src ..."; curl -L -o "$owl" "$loc"; }
  else
    owl="$loc"
    [[ -f "$owl" ]] || { echo "!! missing local source $owl — download ${src} manually into mirror/"; continue; }
  fi
  echo "MIREOT extract: $src ($(wc -l < "$terms") terms)"
  robot extract --method MIREOT \
    --input "$owl" \
    --term-file "$terms" \
    --output "modules/${src}_import.owl"
done

echo
echo "Done. Import modules are in imports/modules/."
echo "Next: build a cmeo-edit.owl that owns ONLY the native CMEO_ terms + the CMEO-added"
echo "bridging axioms, and imports the modules — then merge+reason into the release cmeo.owl."
echo "See README.md (section 'Assemble the release')."
