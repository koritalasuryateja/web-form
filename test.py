import unittest
import json
from app import app
from users import UserManager

class TestUserManager(unittest.TestCase):
    """ Test suite for UserManager class. """

    def setUp(self):
        """ Set up a UserManager instance for testing. """
        self.user_manager = UserManager()

    def test_user_creation(self):
        """ Test creation of a regular user. """
        user = self.user_manager.create_user("testuser", "Test User")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")

    def test_moderator_creation(self):
        """ Test creation of a moderator. """
        moderator = self.user_manager.create_moderator("moduser", "Mod User")
        self.assertIsNotNone(moderator)
        self.assertEqual(moderator.username, "moduser")
        self.assertTrue(moderator.is_moderator)

    def test_user_validation(self):
        """ Test user validation logic. """
        user = self.user_manager.create_user("validuser", "Valid User")
        self.assertTrue(self.user_manager.validate_user(user.user_id, user.key))
        self.assertFalse(self.user_manager.validate_user(user.user_id, "incorrect_key"))

    def test_user_retrieval(self):
        """ Test retrieval of a user. """
        user = self.user_manager.create_user("existinguser", "Existing User")
        self.assertEqual(self.user_manager.get_user(user.user_id), user)

        non_existent_user = self.user_manager.get_user(9999)  # Assuming ID 9999 doesn't exist
        self.assertIsNone(non_existent_user)

class TestFlaskApi(unittest.TestCase):
    """ Test suite for Flask API endpoints. """

    def setUp(self):
        """ Set up a test client for Flask application. """
        app.testing = True
        self.client = app.test_client()
        self.user_manager = UserManager()

    def test_create_user_endpoint(self):
        """ Test the endpoint for creating a user. """
        response = self.client.post('/user', json={'username': 'testuser'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'testuser')

    def test_create_moderator_endpoint(self):
        """ Test the endpoint for creating a moderator. """
        response = self.client.post('/create_moderator',
                                    headers={'Admin-Key': 'admin_key'},
                                    json={'username': 'newmod', 'real_name': 'New Mod'})
        self.assertEqual(response.status_code, 201)

    def test_post_creation_endpoint(self):
        """ Test the endpoint for creating a post. """
        response = self.client.post('/post', json={'msg': 'Test Post'})
        self.assertEqual(response.status_code, 201)

    def test_post_delete_endpoint(self):
        """ Test the endpoint for deleting a post. """
        # Create a post
        create_response = self.client.post('/post', json={'msg': 'Test Post'})
        self.assertEqual(create_response.status_code, 201)
        self.assertTrue('id' in create_response.json)
        self.assertTrue('key' in create_response.json)
       
        post_id = create_response.json['id']
        key = create_response.json['key']
       
        # Delete the post
        delete_response = self.client.delete(f'/post/{post_id}/delete/{key}')
        self.assertEqual(delete_response.status_code, 200)

    def test_post_read_endpoint(self):
        """ Test the endpoint for reading a post. """
        # Assuming a post with ID 1 exists
        response = self.client.get('/post/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
