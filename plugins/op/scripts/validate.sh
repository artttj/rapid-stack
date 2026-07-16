#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
fail=0
for c in commands/*.md; do
  grep -q '^description:' "$c" || { echo "missing description: $c"; fail=1; }
  name=$(basename "$c" .md)
  [ -f "skills/$name/SKILL.md" ] || { echo "missing skill for: $c"; fail=1; }
done
[ -f skills/using-op/SKILL.md ] || { echo "missing using-op skill"; fail=1; }
[ -f skills/project-recipes/SKILL.md ] || { echo "missing project-recipes skill"; fail=1; }
python3 -m json.tool < .claude-plugin/plugin.json > /dev/null || { echo "bad plugin.json"; fail=1; }
python3 -m json.tool < hooks/hooks.json > /dev/null || { echo "bad hooks.json"; fail=1; }
[ "$fail" -eq 0 ] && echo "op validate: OK"
exit "$fail"
