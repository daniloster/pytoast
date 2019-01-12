set -e
set -u
CURRENT_DIR="$(pwd)"

function get_version {
  cat setup.py | grep "version" | cut -d "'" -f 2 | grep "."
}

function bump {
  if [ "$TYPE_RELEASE" == "no-release" ]; then
    echo "- We are skipping releasing"
    exit 0
  fi

  export TYPE_RELEASE="$(git log --no-merges -n 1 --pretty=%B | grep '\[release=' | awk '{print $1}' | sed s/release=// | sed s/[][]//g)"
  CURRENT_VERSION="$(get_version)"
  pipenv run bumpversion --current-version $CURRENT_VERSION $TYPE_RELEASE setup.py
  git add setup.py
  RELEASE_VERSION="$(get_version)"

  cat README.md | sed "s/Version\@$CURRENT_VERSION/Version\@$RELEASE_VERSION/" | sed "s/pytoast==$CURRENT_VERSION/pytoast==$RELEASE_VERSION/"  > './README.md'
  git add README.md

  echo "[skip ci] [release]: v${RELEASE_VERSION}"
  git commit -m "[skip ci] [release]: v${RELEASE_VERSION}"
  git tag -a "v${RELEASE_VERSION}"
  git push gh-publish master --tags
}

function release {
  rm -rf dist/
  rm -rf bdist_wheel/

  pipenv run python setup.py sdist bdist_wheel
  pipenv run twine upload dist/*
}

# Validating if it is a PR
if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then
  echo "- We are in a pull request, not releasing"
  exit 0
fi

# Checking if it is a master commit with release attribute
if [[ $TRAVIS_BRANCH == 'master' ]]; then
  echo '** Setting github user'
  git config --global user.email "daniloster@gmail.com"
  git config --global user.name "Danilo Castro"
  git remote add gh-publish "https://${GIT_AUTH_TOKEN}@github.com/daniloster/pytoast.git"
  git fetch gh-publish
  git checkout master
  git rebase gh-publish/master

  bump()
  release()
fi


function finish {
  cd "$CURRENT_DIR"
}

trap finish EXIT
