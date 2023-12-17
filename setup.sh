#!/bin/sh

pip3 install Flask flask-sqlalchemy flask-login flask-limiter marshmallow werkzeug

# Install or update NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

# Source NVM in the current shell
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  

# Install Node.js 16.x
nvm install 16

# Use Node.js 16.x
nvm use 16

# Install Newman
npm install -g newman
