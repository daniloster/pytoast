set -e
set -u
CURRENT_DIR="$(pwd)"
# Coverage generation based on unit tests
(CURRENT_DIR="$(pwd)" && PYTHONPATH="$CURRENT_DIR" pipenv run python -m coverage run --source "$CURRENT_DIR" --branch --omit="$CURRENT_DIR/pytoast/tests/coverage/*,$CURRENT_DIR/pytoast/tests/*,$CURRENT_DIR/setup.py,.venv/lib/python3.6/site-packages/*" -m  unittest discover -p "test_*.py")
# Reporting coverage
CURRENT_DIR="$(pwd)" && PYTHONPATH="$CURRENT_DIR" pipenv run python -m coverage report
CURRENT_DIR="$(pwd)" && PYTHONPATH="$CURRENT_DIR" pipenv run python -m coverage html -d .coverage_html

function finish {
  cd "$CURRENT_DIR"
}

trap finish EXIT
