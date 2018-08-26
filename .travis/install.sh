#!/bin/bash

# thanks to https://pythonhosted.org/CodeChat/.travis.yml.html article
if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    brew update
    brew install openssl readline
    brew outdated pyenv || brew upgrade pyenv
    brew install pyenv-virtualenv
    pyenv install $PYTHON
    export PYENV_VERSION=$PYTHON
    export PATH="/Users/travis/.pyenv/shims:${PATH}"
    pyenv-virtualenv venv
    source venv/bin/activate
    python --version
else
    sudo add-apt-repository ppa:jonathonf/python-3.5
    sudo apt-get update
    sudo apt-get install python3.5
    python3 --version
fi