from flask import Flask, request, jsonify, abort
from datetime import datetime, timedelta
import os
import threading
from users import UserManager

app = Flask(__name__)

posts = {}
block_ban_list = {}
post_id = 0
user_manager = UserManager()
lock = threading.Lock()
admin_key = "admin_key"

@app.before_request
def check_block_ban_status():
    ip_address = request.remote_addr
    if ip_address in block_ban_list:
        expiry_time = block_ban_list[ip_address]['expiry']
        if datetime.utcnow() <= expiry_time:
            abort(403, "Blocked or Banned")
        else:
            del block_ban_list[ip_address]

@app.route('/create_moderator', methods=['POST'])
def create_moderator():
    if request.headers.get('Admin-Key') != admin_key:
        abort(403, "Unauthorized")
    return jsonify(message='Moderator created successfully'), 201

@app.route('/user', methods=['POST'])
def create_user():
    content = request.json or {}
    username = content.get('username')
    real_name = content.get('real_name', None)

    if not username:
        abort(400, "Username is required")

    try:
        new_user = user_manager.create_user(username, real_name)
    except ValueError as e:
        abort(400, str(e))

    return jsonify(user_id=new_user.user_id, user_key=new_user.key, username=new_user.username), 201

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_metadata(user_id):
    user = user_manager.get_user(user_id)
    if not user:
        abort(404, "User not found")

    return jsonify(user_id=user.user_id, username=user.username, real_name=user.real_name), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def edit_user_metadata(user_id):
    content = request.json or {}
    user_key = content.get('user_key')
    new_real_name = content.get('real_name')

    if not user_manager.validate_user(user_id, user_key):
        abort(403, "Invalid user ID or key")

    user = user_manager.get_user(user_id)
    if new_real_name:
        user.real_name = new_real_name

    return jsonify(user_id=user.user_id, username=user.username, real_name=user.real_name), 200

@app.route('/posts', methods=['GET'])
def get_posts_by_date():
    start = request.args.get('start')
    end = request.args.get('end')

    try:
        start = datetime.fromisoformat(start) if start else None
        end = datetime.fromisoformat(end) if end else None
    except ValueError:
        abort(400, "Invalid date format. Use ISO 8601 format.")

    filtered_posts = []
    with lock:
        for post in posts.values():
            post_time = datetime.fromisoformat(post['timestamp'])
            if (not start or post_time >= start) and (not end or post_time <= end):
                filtered_posts.append(post)

    return jsonify(filtered_posts), 200

@app.route('/post', methods=['POST'])
def create_post():
    global post_id
    content = request.json or {}
    msg = content.get('msg')
    user_id = content.get('user_id')
    user_key = content.get('user_key')

    if not msg:
        abort(400, "Message is required")

    with lock:
        if user_id and user_key and user_manager.validate_user(user_id, user_key):
            post_id += 1
            key = os.urandom(24).hex()
            timestamp = datetime.utcnow().isoformat()
            post = {'id': post_id, 'key': key, 'timestamp': timestamp, 'msg': msg, 'user_id': user_id}
            posts[post_id] = post
            return jsonify(post), 201
        abort(403, "Invalid user ID or key")

@app.route('/post/<int:post_id>', methods=['GET'])
def read_post(post_id):
    with lock:
        post = posts.get(post_id)
        if not post:
            abort(404, "Post not found")

        user_data = None
        if post.get('user_id'):
            user = user_manager.get_user(post['user_id'])
            if user:
                user_data = {'user_id': user.user_id, 'username': user.username}
        return jsonify(id=post['id'], timestamp=post['timestamp'], msg=post['msg'], user=user_data), 200

@app.route('/post/<int:post_id>/delete/<key>', methods=['DELETE'])
def delete_post(post_id, key):
    with lock:
        post = posts.get(post_id)
        if not post:
            abort(404, "Post not found")

        # Moderator deletion check
        if any(user.mod_key == key and user.is_moderator for user in user_manager.users.values()):
            del posts[post_id]
            return jsonify(status="Post deleted by moderator")

        # User deletion check
        if post['key'] == key or (post.get('user_id') and user_manager.validate_user(post['user_id'], key)):
            del posts[post_id]
            return jsonify(status="Post deleted")

        abort(403, "Forbidden: Invalid key")

if __name__ == '__main__':
    app.run(debug=True)
