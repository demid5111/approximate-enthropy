#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then

    # Install some custom requirements on OS X
    # e.g. brew install pyenv-virtualenv

    case "${TOXENV}" in
        py35)
            # Install some custom Python 3.2 requirements on OS X
            brew install python3
            ;;
    esac
fi

pip3 install -r requirements.txt