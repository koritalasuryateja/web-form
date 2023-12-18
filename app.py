from flask import Flask, jsonify, request
from models import User, Post
from database import db_session
from datetime import datetime
import secrets
import re

app = Flask(__name__)

# Helper function to generate a unique user key
def generate_unique_key():
    return secrets.token_urlsafe(16)

@app.route('/posts/search', methods=['GET'])
def search_posts():
    query = request.args.get('query', '')
    matched_posts = Post.search(query)
    return jsonify(matched_posts)

@app.route('/posts/date-range', methods=['GET'])
def posts_date_range():
    start = request.args.get('start')
    end = request.args.get('end')
    filtered_posts = Post.get_by_date_range(start, end)
    return jsonify(filtered_posts)

@app.route('/register', methods=['POST'])
def register_user():
    user_details = request.get_json()
    user = User.create(user_details)
    if user is None:
        return jsonify(error='Failed to create user.'), 400
    return jsonify(user), 200

@app.route('/user/<user_identifier>', methods=['GET'])
def get_user(user_identifier):
    user = User.get(user_identifier)
    if user is None:
        return jsonify(error='User not found.'), 404
    return jsonify(user), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    update_data = request.get_json()
    success = User.update(user_id, update_data)
    if not success:
        return jsonify(error='Failed to update user.'), 400
    return jsonify(message='User information updated successfully.'), 200

@app.route('/post', methods=['POST'])
def create_post():
    post_data = request.get_json()
    post = Post.create(post_data)
    if post is None:
        return jsonify(error='Failed to create post.'), 400
    return jsonify(post), 200

@app.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.get(post_id)
    if post is None:
        return jsonify(error='Post not found.'), 404
    return jsonify(post), 200

@app.route('/post/<int:post_id>/delete/<post_key>', methods=['DELETE'])
def delete_post(post_id, post_key):
    success = Post.delete(post_id, post_key)
    if not success:
        return jsonify(error='Failed to delete post.'), 400
    return jsonify(message='Post deleted successfully.'), 200

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)
