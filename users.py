import os

class User:
    """ Represents a user in the system. """
    def __init__(self, user_id, key, username, real_name=None, is_moderator=False, mod_key=None):
        self.user_id = user_id
        self.key = key
        self.username = username
        self.real_name = real_name
        self.is_moderator = is_moderator
        self.mod_key = mod_key if is_moderator else None

class UserManager:
    """ Manages user creation and validation in the system. """
    def __init__(self):
        self.users = {}
        self.next_user_id = 1

    def _create_user(self, username, real_name, is_moderator=False):
        """ Creates a generic user, used internally for both users and moderators. """
        if any(user.username == username for user in self.users.values()):
            raise ValueError("Username already exists")

        user_key = os.urandom(24).hex()
        mod_key = os.urandom(24).hex() if is_moderator else None
        new_user = User(self.next_user_id, user_key, username, real_name, is_moderator, mod_key)
        self.users[self.next_user_id] = new_user
        self.next_user_id += 1
        return new_user

    def create_moderator(self, username, real_name):
        """ Creates a moderator with unique keys. """
        return self._create_user(username, real_name, is_moderator=True)

    def create_user(self, username, real_name):
        """ Creates a regular user. """
        return self._create_user(username, real_name)

    def validate_user(self, user_id, key):
        """ Validates if the user_id and key combination is correct. """
        return user_id in self.users and self.users[user_id].key == key

    def get_user(self, user_id):
        """ Retrieves a user by their ID. """
        return self.users.get(user_id)
