#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    nvm ls
    nvm install lts/carbon
    nvm use lts/carbon
    node --version
    npm install -g create-dmg
else
    sudo apt-get update
    sudo apt-get install -y xvfb herbstluftwm
    export DISPLAY=:99.0
    /sbin/start-stop-daemon --start --quiet --pidfile /tmp/custom_xvfb_99.pid --make-pidfile --background --exec /usr/bin/Xvfb -- :99 -screen 0 1920x1200x24 -ac +extension GLX +render -noreset
    sleep 3
fi
pip3 install -r requirements.txt