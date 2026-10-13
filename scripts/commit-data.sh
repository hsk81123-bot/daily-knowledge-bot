#!/usr/bin/env bash
# data/ 변경분(발송 기록, 공부 노트)을 커밋하고 push한다. 동시 실행 충돌에 대비해 rebase 후 재시도한다.
set -euo pipefail

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

git add -A data/
if git diff --cached --quiet; then
  echo "변경된 기록이 없습니다."
  exit 0
fi
git commit -m "${1:-chore: 공부 노트 기록 업데이트}"

for attempt in 1 2 3 4; do
  if git push; then
    exit 0
  fi
  echo "push 실패(${attempt}회). 원격 변경을 rebase 후 재시도합니다."
  sleep $((attempt * 5))
  git pull --rebase
done
echo "push에 4번 실패했습니다." >&2
exit 1
