export CURRENT_DIR="$(pwd)"

function finish {
  cd "$CURRENT_DIR"
}

sh bin/setup_pipenv.sh

trap finish EXIT
