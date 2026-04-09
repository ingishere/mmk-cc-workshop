#!/bin/bash
# Install libraries needed for this project
# Runs at SessionStart — only in remote environments

# Only run in remote environments
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

echo "=== Installing Libraries ==="

# Python dependencies
if [ -f "requirements.txt" ]; then
  echo "pip       : installing requirements..."
  pip3 install -q -r requirements.txt 2>/dev/null || echo "pip       : FAILED"
fi

# mmk: Magic Meal Kits CLI (YouTube transcript, metadata, etc.)
if command -v mmk >/dev/null 2>&1; then
  echo "mmk       : $(mmk version 2>/dev/null || echo 'installed') (already installed)"
else
  echo "mmk       : installing..."
  npm install -g @magic-meal-kits/cli 2>/dev/null || {
    echo "mmk       : FAILED (npm not available)"
    echo "=== Done ==="
    exit 0
  }
  echo "mmk       : $(mmk version 2>/dev/null || echo 'installed')"
fi

echo "=== Done ==="
exit 0
