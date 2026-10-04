#!/usr/bin/env bash
# 사용법: _dev/wait.sh <path> [grep-pattern]
# 로컬 Jekyll 서버가 <path>를 200으로 서빙하고, 패턴이 있으면 응답에 패턴이 나타날 때까지 최대 180초 기다린다.
set -euo pipefail
BASE="${SITE_BASE_URL:-http://localhost:4000}"
PATH_ARG="${1:-/}"
PATTERN="${2:-}"
for _ in $(seq 1 90); do
  if body="$(curl -sf "${BASE}${PATH_ARG}")"; then
    if [ -z "${PATTERN}" ] || grep -q -- "${PATTERN}" <<<"${body}"; then
      echo "ready: ${BASE}${PATH_ARG}"
      exit 0
    fi
  fi
  sleep 2
done
echo "timeout waiting for ${BASE}${PATH_ARG} ${PATTERN}" >&2
exit 1
