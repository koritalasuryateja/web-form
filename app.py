
from flask import Flask, request, jsonify, abort
import secrets
from datetime import datetime

app = Flask(__name__)

posts = {}
next_id = 1  # Initialize next_id
master_key = "your_master_key_here"  # Set your master key

class User:
    def __init__(self, username, email, real_name, avatar_icon):
        self.id = next_user_id
        self.username = username
        self.email = email
        self.real_name = real_name
        self.avatar_icon = avatar_icon
        self.posts = []  # Store posts created by this user
        next_user_id += 1  # Increment next_user_id

# Create a sample user
sample_user = User("user1", "user1@example.com", "John Doe", "avatar1")
users = {sample_user.id: sample_user}  # Initialize users dictionary

@app.route('/add_moderator', methods=['POST'])
def add_moderator():
    if request.headers.get('Master-Key') != master_key:
        abort(403, description="Not Authorized")
    return jsonify({'response': 'Moderator added successfully'}), 201


@app.route('/post', methods=['POST'])
def create_post():
    global next_id
    if not request.is_json:
        return "Invalid format, JSON required", 400

    data = request.get_json()
    if 'msg' not in data or not isinstance(data['msg'], str):
        return "Bad request: 'msg' field missing or not a string", 400

    key = secrets.token_urlsafe(16)
    timestamp = datetime.utcnow().isoformat() + "Z"
    posts[next_id] = {'msg': data['msg'], 'key': key, 'timestamp': timestamp}
    
    response = {'id': next_id, 'key': key, 'timestamp': timestamp}
    next_id += 1
    return jsonify(response)



@app.route('/post/<int:post_id>', methods=['GET'])
def read_post(post_id):
    post = posts.get(post_id)
    if post is None:
        return "Post not found", 404

    response = {
        'id': post_id,
        'timestamp': post['timestamp'],
        'msg': post['msg']
    }
    return jsonify(response)


@app.route('/post/<int:post_id>/delete/<key>', methods=['DELETE'])
def delete_post(post_id, key):
    post = posts.get(post_id)
    if post is None:
        return "Post not found", 404

    if post['key'] != key:
        return "Forbidden: Incorrect key", 403

    del posts[post_id]
    return jsonify({'id': post_id, 'key': key, 'timestamp': post['timestamp']})



if __name__ == '__main__':
    app.run(debug=True)
