#!/usr/bin/env bash
set -euo pipefail

RUN_FILE=${1:-"_run300_next.json"}
PREFIX=${2:-"wf_r3_next_chunk"}
N=${3:-60}
WORKFLOW_CMD=${WORKFLOW_CMD:-}

if [[ -z "${WORKFLOW_CMD}" ]]; then
  echo "WORKFLOW_CMD must be set to the workflow runner invocation."
  echo "Example: WORKFLOW_CMD=\"your_runner --flags\" ./run_next_chunk_sequence.sh"
  exit 1
fi

for i in 1 2 3 4 5; do
  idx=$(( (i-1)*N ))
  script="${PREFIX}${i}.js"
  out="${script%.js}.output"
  echo "Running ${script}"
  bash -lc "${WORKFLOW_CMD} \"Workflow({scriptPath:'${script}')\"" > "${out}" 2>&1 || true
  if grep -q "You've hit your weekly limit" "${out}"; then
    echo "weekly limit hit at ${script}; stop"
    exit 1
  fi
  python3 harvest_wf.py "${out}" "briefs_r3_${i}.json" ${N} ${idx} "${RUN_FILE}"
  echo "${script} -> briefs_r3_${i}.json"
done
