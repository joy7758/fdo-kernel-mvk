#!/usr/bin/env bash
set -euo pipefail

reset_state() {
  cat > object.json <<'JSON'
{
  "id": "",
  "input": "hello-mvk",
  "payload": "sha256",
  "state": "init",
  "constraint": "hash-match",
  "signature": ""
}
JSON

  cat > trace.json <<'JSON'
{
  "previous_hash": "GENESIS",
  "current_hash": "",
  "object_signature": "",
  "status": "UNINITIALIZED"
}
JSON
}

assert_last_line() {
  local output="$1"
  local expected="$2"
  local actual
  actual="$(printf '%s\n' "$output" | tail -n 1)"
  if [[ "$actual" != "$expected" ]]; then
    printf 'ASSERT_FAIL expected=%s actual=%s\n' "$expected" "$actual"
    exit 1
  fi
}

reset_state

for _ in 1 2 3; do
  run_output="$(make run)"
  replay_output="$(make replay)"
  assert_last_line "$run_output" "EXECUTION_OK"
  assert_last_line "$replay_output" "REPLAY_PASS"
done

set +e
tamper_output="$(make tamper 2>&1)"
tamper_code=$?
set -e

if [[ $tamper_code -eq 0 ]]; then
  echo "ASSERT_FAIL tamper should fail-closed"
  exit 1
fi

if ! printf '%s\n' "$tamper_output" | grep -q "CONFORMANCE_FAIL"; then
  echo "ASSERT_FAIL missing CONFORMANCE_FAIL"
  exit 1
fi

reset_state
echo "ALL_TESTS_PASS"
