export CURRENT_DIR="$(pwd)"
export PIPENV_VENV_IN_PROJECT=1
echo "Removing previous python env for $CURRENT_DIR..."
pipenv --rm
echo "Installing python requirements at $CURRENT_DIR..."
if [[ "$TRAVIS_PYTHON_VERSION" == "" ]]; then export TRAVIS_PYTHON_VERSION="3.6.5"; fi
pipenv install -r requirements.txt --python "$TRAVIS_PYTHON_VERSION"
# Preparing setup tools
pipenv install twine
pipenv install wheel
pipenv install bumpversion
