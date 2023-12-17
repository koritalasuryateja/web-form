import os

class ForumMember:
    def __init__(self, member_id, access_key, nickname, moderator=False, moderator_key=None, full_name=None, user_key=None):
        self.member_id = member_id
        self.access_key = access_key
        self.nickname = nickname
        self.moderator = moderator
        self.moderator_key = moderator_key
        self.full_name = full_name
        self.user_key = user_key  # New field for user-specific key

class MemberManager:
    def __init__(self):
        self.members = {}
        self.id_counter = 0

    def create_forum_moderator(self, nickname, full_name):
        self.id_counter += 1
        member_access_key = os.urandom(24).hex()
        moderator_key = os.urandom(24).hex()
        user_key = os.urandom(24).hex()  # Generate a unique user key
        new_member = ForumMember(self.id_counter, member_access_key, nickname, True, moderator_key, full_name, user_key)
        self.members[self.id_counter] = new_member
        return new_member

    def register_member(self, nickname, full_name=None):
        original_nickname = nickname
        nickname_suffix = 1
        while any(member.nickname == nickname for member in self.members.values()):
            nickname = f"{original_nickname}_{nickname_suffix}"
            nickname_suffix += 1

        self.id_counter += 1
        member_access_key = os.urandom(24).hex()
        user_key = os.urandom(24).hex()  # Generate a unique user key
        new_member = ForumMember(self.id_counter, member_access_key, nickname, False, full_name=full_name, user_key=user_key)
        self.members[self.id_counter] = new_member
        return new_member

    def validate_member(self, member_id, provided_key):
        member = self.members.get(member_id)
        return member and (member.access_key == provided_key or member.user_key == provided_key)

    def get_member_info(self, member_id):
        return self.members.get(member_id)

    def validate_user(self, user_id):
        return user_id in self.members

   
