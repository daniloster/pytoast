set -e
set -u
CURRENT_DIR="$(pwd)"
# unit tests
# pipenv run python -m unittest discover -p "test_*.py"
(CURRENT_DIR="$(pwd)" && PYTHONPATH="$CURRENT_DIR" pipenv run python -m coverage run --source "$CURRENT_DIR" --branch --omit="$CURRENT_DIR/pytoast/tests/coverage/*,$CURRENT_DIR/pytoast/tests/*,$CURRENT_DIR/setup.py,.venv/lib/python3.6/site-packages/*" -m  unittest discover -p "test_*.py")
# Coverage generation
# (CURRENT_DIR="$(pwd)" && PYTHONPATH="$CURRENT_DIR" pipenv run python -m coverage run --source "$CURRENT_DIR" --branch --omit="$CURRENT_DIR/pytoast/tests/coverage/*,$CURRENT_DIR/pytoast/tests/*,$CURRENT_DIR/setup.py,.venv/lib/python3.6/site-packages/*" $CURRENT_DIR/pytoast/tests/coverage/all_success/run.py --root="$CURRENT_DIR" --features="$CURRENT_DIR/pytoast/tests/coverage/all_success/features" --verbose)
# (CURRENT_DIR="$(pwd)" && PYTHONPATH="$CURRENT_DIR" pipenv run python -m coverage run --append --source "$CURRENT_DIR" --branch --omit="$CURRENT_DIR/pytoast/tests/coverage/*,$CURRENT_DIR/pytoast/tests/*,$CURRENT_DIR/setup.py,.venv/lib/python3.6/site-packages/*" $CURRENT_DIR/pytoast/tests/coverage/one_fail/run.py --root="$CURRENT_DIR" --features="$CURRENT_DIR/pytoast/tests/coverage/one_fail/features" --verbose) || echo 'Skipping failure scenarios for coverage'
# (CURRENT_DIR="$(pwd)" && PYTHONPATH="$CURRENT_DIR" pipenv run python -m coverage run --append --source "$CURRENT_DIR" --branch --omit="$CURRENT_DIR/pytoast/tests/coverage/*,$CURRENT_DIR/pytoast/tests/*,$CURRENT_DIR/setup.py,.venv/lib/python3.6/site-packages/*" $CURRENT_DIR/pytoast/tests/coverage/one_fail/run.py --root="$CURRENT_DIR" --features="$CURRENT_DIR/pytoast/tests/coverage/one_fail/features" --verbose --fail-fast) || echo 'Skipping failure scenarios for coverage with --fail-fast'
# Reporting coverage
CURRENT_DIR="$(pwd)" && PYTHONPATH="$CURRENT_DIR" pipenv run python -m coverage report
CURRENT_DIR="$(pwd)" && PYTHONPATH="$CURRENT_DIR" pipenv run python -m coverage html -d .coverage_html


function finish {
  cd "$CURRENT_DIR"
}

trap finish EXIT
