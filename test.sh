#!/bin/sh

# Source NVM in the current shell
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Use the correct Node.js version with NVM
nvm use 16

# Set the Flask app environment variable
export FLASK_APP=server.py  # Replace with your actual Flask app filename

# Exit immediately if any command fails
set -e

# Start the Flask server in the background
flask run &
#PID=$!  # Record the PID of the Flask server

python3 server.py &
APP_PID=$!
python3 test.py

# Allow some time for the server to start
sleep 5

# Run Newman tests
echo "Running Newman tests for multiple posts..."
newman run forum_multiple_posts.postman_collection.json -e env.json

echo "Running Newman tests for post read and delete..."
newman run forum_post_read_delete.postman_collection.json -n 50

# Kill the Flask server process
kill $APP_PID

echo "Tests completed."

# Exit
exit 0
