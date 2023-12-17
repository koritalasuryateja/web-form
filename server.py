from flask import Flask, request, jsonify, abort
import datetime
import threading
from web_users import MemberManager
from datetime import datetime as dt, timedelta
import os

forum_app = Flask(__name__)

discussion_posts = {}
attempt_failures = {}
ip_restrict_list = {}
unique_post_id = 0
member_manager = MemberManager()
sync_lock = threading.Lock()
master_key = "admin_key"

def is_ip_restricted_or_blocked(ip):
    if ip in ip_restrict_list:
        block_expiry = ip_restrict_list[ip]['expiry']
        if dt.utcnow() <= block_expiry:
            return True
        else:
            del ip_restrict_list[ip]
    return False

@forum_app.before_request
def verify_ip_status():
    client_ip = request.remote_addr
    if is_ip_restricted_or_blocked(client_ip):
        abort(403, description="IP Restricted or Blocked")

@forum_app.route('/add_moderator', methods=['POST'])
def add_moderator():
    if request.headers.get('Master-Key') != master_key:
        abort(403, description="Not Authorized")
    return jsonify({'response': 'Moderator added successfully'}), 201


@forum_app.route('/member', methods=['POST'])
def register_member():
    data = request.json
    member_name = data.get('member_name')
    full_name = data.get('full_name', None)

    if not member_name:
        abort(400, description="Member name required")

    new_member = member_manager.register_member(member_name, full_name)
    return jsonify(member_id=new_member.member_id, member_key=new_member.access_key, member_name=new_member.nickname)

@forum_app.route('/member/<int:member_id>', methods=['GET'])
def get_member_info(member_id):
    member = member_manager.get_member_info(member_id)
    if member:
        return {'member_name': member.nickname, 'full_name': member.full_name}
    else:
        return jsonify(message='Member not found'), 404

@forum_app.route('/member/<int:member_id>/edit', methods=['PUT'])
def update_member_info(member_id):
    data = request.json
    member_access_key = data.get('member_key')
    updated_full_name = data.get('full_name')

    if not member_manager.validate_member(member_id, member_access_key):
        abort(403, description="Invalid member ID or key")

    member_info = member_manager.get_member_info(member_id)
    if not member_info:
        abort(404, description='Member not found')
    member = member_info
    if updated_full_name:
        member.full_name = updated_full_name

    return jsonify(member_id=member.member_id, member_name=member.nickname, full_name=member.full_name)

@forum_app.route('/discussions', methods=['GET'])
def filter_posts_by_year():
    year = request.args.get('year')

    try:
        if year:
            year = int(year)
    except ValueError:
        abort(400, description="Invalid year format. Use a valid year (e.g., 2023).")

    selected_posts = []
    with sync_lock:
        for post in discussion_posts.values():
            post_year = dt.fromisoformat(post['timestamp']).year
            if not year or post_year == year:
                selected_posts.append(post)

    return jsonify(selected_posts)

@forum_app.route('/discussions/member/<int:member_id>', methods=['GET'])
def filter_posts_by_member(member_id):
    with sync_lock:
        member_discussions = [post for post in discussion_posts.values() if post.get('member_id') == member_id]
    
    return jsonify(member_discussions)

@forum_app.route('/discussion', methods=['POST'])
def add_post():
    global unique_post_id
    data = request.json

    if not data or 'message' not in data or not isinstance(data['message'], str):
        return jsonify(error="Bad Request"), 400
    
    member_id = data.get('member_id')
    member_key = data.get('member_key')

    if member_id and member_key:
        with sync_lock:
            if member_manager.validate_member(member_id, member_key):
                unique_post_id += 1
                secure_key = os.urandom(24).hex()
                time_stamp = dt.utcnow().isoformat()
                discussion = {'id': unique_post_id, 'key': secure_key, 'timestamp': time_stamp, 'message': data['message'], 'member_id': member_id}
                discussion_posts[unique_post_id] = discussion
                return jsonify(discussion)
            else:
                abort(403, description="Invalid member ID or key")

    with sync_lock:
        unique_post_id += 1
        secure_key = os.urandom(24).hex()
        time_stamp = dt.utcnow().isoformat()
        discussion_posts[unique_post_id] = {'id': unique_post_id, 'key': secure_key, 'timestamp': time_stamp, 'message': data['message']}

    return jsonify(id=unique_post_id, key=secure_key, timestamp=time_stamp)

@forum_app.route('/discussion/<int:post_id>', methods=['GET'])
def view_post(post_id):
    with sync_lock:
        if post_id in discussion_posts:
            discussion = discussion_posts[post_id]
            member_id = discussion.get('member_id')
            member_info = None
            if member_id:
                member = member_manager.get_member(member_id)
                if member:
                    member_info = {'member_id': member.member_id, 'member_name': member.nickname}
            return jsonify(id=discussion['id'], timestamp=discussion['timestamp'], message=discussion['message'], member=member_info)
        else:
            abort(404, description="Discussion not found")

@forum_app.route('/discussion/<int:post_id>/remove/<key>', methods=['DELETE'])
def remove_post(post_id, key):
    with sync_lock:
        if post_id not in discussion_posts:
            abort(404, description="Discussion not found")

        discussion = discussion_posts[post_id]
        if any(member.mod_access_key == key and member.moderator_status for member in member_manager.members.values()):
            del discussion_posts[post_id]
            return jsonify(status="Discussion removed by moderator")
        if discussion['key'] == key or (discussion.get('member_id') and member_manager.validate_member(discussion.member_id, key)):
            del discussion_posts[post_id]
            return jsonify(id=post_id, key=key, timestamp=discussion['timestamp'])
        else:
            abort(403, description="Forbidden: Invalid key")

@forum_app.route('/discussion/<int:post_id>/edit', methods=['PUT'])
def edit_post(post_id):
    content = request.json
    member_id = content.get('member_id')
    member_key = content.get('member_key')
    new_message = content.get('new_message')

    # Check if the member is authorized to edit the post
    with sync_lock:
        if post_id in discussion_posts:
            discussion = discussion_posts[post_id]
            discussion['message'] = new_message
            return jsonify(id=discussion['id'], timestamp=discussion['timestamp'], message=new_message, member_id=member_id)
            '''if discussion.get('member_id') == member_id:
                # Validate the member's access key
                if member_manager.validate_member(member_id, member_key):
                    # Update the post message
                    discussion['message'] = new_message
                    return jsonify(id=discussion['id'], timestamp=discussion['timestamp'], message=new_message, member_id=member_id)
                else:
                    abort(403, description="Invalid member ID or key")
            else:
                abort(405, description="You do not have permission to edit this post")'''
        else:
            abort(404, description="Post not found")


@forum_app.route('/user/<int:user_id>/update', methods=['PUT'])
def update_user_profile(user_id):
    content = request.json
    user_key = content.get('user_key')
    new_real_name = content.get('new_real_name')

    if not member_manager.validate_user(user_id):
        abort(403, description="Invalid user ID or key")

    user = member_manager.get_member_info(user_id)
    if user:
        user.real_name = new_real_name
        return jsonify(user_id=user.member_id, username=user.nickname, real_name=user.full_name)
    else:
        abort(404, description="User not found")

@forum_app.route('/posts/search', methods=['GET'])
def search_posts():
    keyword = request.args.get('keyword')
    filtered_posts = [post for post in discussion_posts.values() if keyword.lower() in post.get('msg', '').lower()]
    return jsonify(filtered_posts)



if __name__ == '__main__':
    forum_app.run(debug=True)

# Additional corrections and logic adjustments
# TODO: Implement specific corrections based on the application's requirements and logic

# Placeholder for potential corrections in server.py
# TODO: Review and correct authorization logic, request formatting, and response handling
