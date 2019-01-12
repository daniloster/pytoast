set -e
set -u
CURRENT_DIR="$(pwd)"

# Validating if it is a PR
if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then
  echo "[ci] we are in a pull request, not releasing"
  exit 0
fi

# Checking if it is a master commit with release attribute
if [[ $TRAVIS_BRANCH == 'master' ]]; then
  echo "[git] pushing commit and tags"
  git push gh-publish master --tags
fi


function finish {
  cd "$CURRENT_DIR"
}

trap finish EXIT
