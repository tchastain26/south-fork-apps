#!/bin/bash
# Usage: ./tests/validate.sh [app-folder-name]
# Example: ./tests/validate.sh tip-calculator
# Run with no argument to validate all apps in todo.md

COLLECTION="South Fork Apps Collection"
PASS=0
FAIL=0

check_app() {
  local app="$1"
  local dir="$COLLECTION/$app"
  local ok=true

  echo "--- $app ---"

  # index.html exists
  if [ ! -f "$dir/index.html" ]; then
    echo "  FAIL: index.html missing"
    ok=false
  else
    # Theme colors present
    if ! grep -q "#111412" "$dir/index.html"; then
      echo "  FAIL: background color #111412 not found"
      ok=false
    fi
    if ! grep -q "#7ddb84" "$dir/index.html"; then
      echo "  FAIL: accent color #7ddb84 not found"
      ok=false
    fi
    # Nav bar present
    if ! grep -q "southforkapps.com" "$dir/index.html"; then
      echo "  FAIL: nav link to southforkapps.com missing"
      ok=false
    fi
    # Plus Jakarta Sans
    if ! grep -q "Plus Jakarta Sans" "$dir/index.html"; then
      echo "  FAIL: Plus Jakarta Sans font not found"
      ok=false
    fi
    echo "  OK: index.html"
  fi

  # Notes.md exists
  local notes=$(ls "$dir/"*"Notes.md" 2>/dev/null | head -1)
  if [ -z "$notes" ]; then
    echo "  FAIL: Notes.md missing"
    ok=false
  else
    echo "  OK: Notes.md"
  fi

  if $ok; then
    echo "  PASS"
    ((PASS++))
  else
    ((FAIL++))
  fi
  echo ""
}

# Single app mode
if [ -n "$1" ]; then
  check_app "$1"
  exit 0
fi

# All apps mode
APPS=(
  "tip-calculator"
  "pomodoro-timer"
  "password-generator"
  "age-calculator"
  "word-counter"
  "debt-snowball"
  "random-picker"
  "unit-converter"
  "habit-tracker"
  "countdown-timer"
)

for app in "${APPS[@]}"; do
  check_app "$app"
done

echo "=============================="
echo "Results: $PASS passed, $FAIL failed"
