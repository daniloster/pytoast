export CURRENT_DIR="$(pwd)"
export PIPENV_VENV_IN_PROJECT=1
echo "Removing previous python env for $CURRENT_DIR..."
pipenv --rm
echo "Installing python requirements at $CURRENT_DIR..."
pipenv install -r requirements.txt --python 3.6.5
