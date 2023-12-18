from flask import Flask, jsonify, request
from datetime import datetime
import threading
import secrets
import re

app = Flask(__name__)

# Global variables for storing user and post data
user_counter = 0
post_counter = 0
user_storage = {}
post_storage = {}
data_access_lock = threading.Lock()

def generate_unique_key():
    """Generate a unique key using a secure token."""
    return secrets.token_urlsafe(16)

@app.route('/posts/search', methods=['GET'])
def search_posts():
    """Endpoint for searching posts based on a query."""
    query = request.args.get('query', '')
    with data_access_lock:
        # Filter posts that match the query
        matched_posts = [post for post in post_storage.values() if re.search(query, post['msg'], re.IGNORECASE)]
        return jsonify(matched_posts)

@app.route('/posts/date-range', methods=['GET'])
def posts_date_range():
    """Endpoint for fetching posts within a specific date range."""
    start = request.args.get('start')
    end = request.args.get('end')
    with data_access_lock:
        # Filter posts within the specified date range
        filtered_posts = [post for post in post_storage.values() if start <= post['timestamp'] <= end]
        return jsonify(filtered_posts)

@app.route('/register', methods=['POST'])
def register_user():
    """Endpoint for registering a new user."""
    with data_access_lock:
        if not request.is_json:
            return jsonify(error='Invalid JSON format.'), 400

        user_details = request.get_json()
        name = user_details.get('name')
        username = user_details.get('username')

        if not name or not isinstance(name, str) or not username or not isinstance(username, str):
            return jsonify(error='Name and username are required and must be strings.'), 400

        if any(user['username'] == username for user in user_storage.values()):
            return jsonify(error='Username already in use.'), 400

        global user_counter
        user_counter += 1
        user_key = generate_unique_key()
        user_storage[user_counter] = {'id': user_counter, 'name': name, 'username': username, 'key': user_key}

        return jsonify(id=user_counter, key=user_key), 200

@app.route('/user/<user_identifier>', methods=['GET'])
def get_user(user_identifier):
    """Endpoint for retrieving user information by ID or username."""
    with data_access_lock:
        user = user_storage.get(int(user_identifier)) if user_identifier.isdigit() else \
               next((u for u in user_storage.values() if u['username'] == user_identifier), None)

        if not user:
            return jsonify(error='User not found.'), 404

        return jsonify({'id': user['id'], 'name': user['name'], 'username': user['username']}), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Endpoint for updating user information."""
    with data_access_lock:
        if user_id not in user_storage:
            return jsonify(error='User not found.'), 404

        update_data = request.get_json()
        if update_data.get('key') != user_storage[user_id].get('key'):
            return jsonify(error='Unauthorized access.'), 401

        user_storage[user_id].update({k: v for k, v in update_data.items() if k in ['name', 'username']})
        return jsonify(message='User updated successfully.'), 200

@app.route('/post', methods=['POST'])
def create_post():
    """Endpoint for creating a new post."""
    with data_access_lock:
        post_data = request.get_json()

        if not post_data.get('msg') or not isinstance(post_data['msg'], str):
            return jsonify(error='Invalid post message.'), 400

        global post_counter
        post_counter += 1
        post_key = generate_unique_key()

        post_details = {
            'id': post_counter, 
            'msg': post_data['msg'], 
            'key': post_key, 
            'timestamp': datetime.utcnow().isoformat()
        }

        if 'file' in post_data:
            try:
                post_details['file'] = post_data['file']
            except Exception as e:
                return jsonify(error=str(e)), 400

        if 'user_id' in post_data and 'user_key' in post_data:
            user_id = post_data['user_id']
            if user_storage.get(user_id, {}).get('key') == post_data['user_key']:
                post_details['user_id'] = user_id
                post_details['username'] = user_storage[user_id]['username']

        post_storage[post_counter] = post_details
        return jsonify(post_details), 200

@app.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    with data_access_lock:
        if post_id not in post_storage:
            return jsonify(error='Post not found.'), 404

        post = post_storage[post_id]
        post_info = {k: v for k, v in post.items() if k != 'key'}
        return jsonify(post_info), 200

# Endpoint to delete a post
@app.route('/post/<int:post_id>/delete/<post_key>', methods=['DELETE'])
def delete_post(post_id, post_key):
    with data_access_lock:
        if post_id not in post_storage or post_storage[post_id]['key'] != post_key:
            return jsonify(error='Invalid post ID or key.'), 403

        deleted_post = post_storage.pop(post_id)
        return jsonify({k: v for k, v in deleted_post.items() if k != 'key'}), 200


if __name__ == '__main__':
    app.run(debug=True)
