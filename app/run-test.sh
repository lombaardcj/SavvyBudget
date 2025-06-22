#!/bin/bash
# Run all backend tests for SavvyBudget

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/backend"

source ../backend-venv/bin/activate
pytest --maxfail=5 -v --verbosity=6 tests
