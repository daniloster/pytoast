set -e
set -u
CURRENT_DIR="$(pwd)"

rm -rf dist/
python setup.py bdist_wheel

function finish {
  cd "$CURRENT_DIR"
}

trap finish EXIT
