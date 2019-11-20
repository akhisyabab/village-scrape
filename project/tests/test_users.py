import json
import unittest

from project import db
from project.models.models import User
from project.tests.base import BaseTestCase


def add_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user


# class TestUserService(BaseTestCase):
#     """Tests for the Users Service."""

    # def test_register_user(self):
    #     """Ensure a new user can be added to the database."""
    #     with self.client:
    #         response = self.client.post(
    #             '/api/v1/register',
    #             data=json.dumps({
    #                 'username': 'username',
    #                 'password': 'password'
    #             }),
    #             content_type='application/json',
    #         )
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn('User created: username', data['message'])
    #
    # def test_register_user_duplicate_username(self):
    #     """Ensure error is thrown if the username already exists."""
    #     self.test_register_user()
    #     with self.client:
    #         response = self.client.post(
    #             '/api/v1/register',
    #             data=json.dumps({
    #                 'username': 'username',
    #                 'password': 'password'
    #             }),
    #             content_type='application/json',
    #         )
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(
    #             'User already exists: username', data['message'])
    #
    # def test_login_user(self):
    #     """Ensure get single user behaves correctly."""
    #     self.test_register_user()
    #     with self.client:
    #         response = self.client.post(
    #             '/api/v1/login',
    #             data=json.dumps({
    #                 'username': 'username',
    #                 'password': 'password'
    #             }),
    #             content_type='application/json',
    #         )
    #         data = json.loads(response.data.decode())
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn('Logged in as username', data['message'])

if __name__ == '__main__':
    unittest.main()
