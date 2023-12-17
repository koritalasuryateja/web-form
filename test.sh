#!/bin/sh

# Source NVM in the current shell
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  

set -e # exit immediately if newman complains
trap 'kill $PID' EXIT # kill the server on exit

./run.sh &
PID=$! # record the PID

# Use the correct Node.js version with NVM
nvm use 16

# Run Newman tests
newman run forum_multiple_posts.postman_collection.json -e env.json # use the env file
newman run forum_post_read_delete.postman_collection.json -n 50 # 50 iterations

# Additional test commands (if needed)
# ...

# Exit
exit 0
