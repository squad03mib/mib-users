# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO
import connexion
from swagger_server.models.authenticate_body import AuthenticateBody  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_listitem import UserListitem  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_mib_resources_auth_authenticate(self):
        """Test case for mib_resources_auth_authenticate

        Authenticate a user
        """
        body = User()
        body.birthdate = "2020-01-01T00:00:00+00:00"
        body.email = "prova@gm.com"
        body.firstname = "gg"
        body.lastname = "gg"
        body.password = "1234ABCD"
        response = self.client.open(
            '/users',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        auth = AuthenticateBody()
        auth.email = body.email
        auth.password = body.password

        response = self.client.open(
            '/authenticate',
            method='POST',
            data=json.dumps(auth),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertIn(b"prova", response.data)

        auth.password = "1234"
        response = self.client.open(
            '/authenticate',
            method='POST',
            data=json.dumps(auth),
            content_type='application/json')
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mib_resources_users_create_user(self):
        """Test case for mib_resources_users_create_user

        Add a new user
        """
        body = User()
        body.birthdate = "2020-01-01T00:00:00+00:00"
        body.email = "fake@gm.com"
        body.firstname = "gg"
        body.lastname = "gg"
        body.password = "password"
        response = self.client.open(
            '/users',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertIn("fake@gm.com", response.data.decode('utf-8'))

        # retry to create a user with same mail
        response = self.client.open(
            '/users',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert403(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mib_resources_users_get_user(self):
        """Test case for mib_resources_users_get_user


        """
        response = self.client.open(
            '/users/{user_id}'.format(user_id=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        response = self.client.open(
            '/users/{user_id}'.format(user_id=789),
            method='GET')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mib_resources_users_get_user_by_email(self):
        """Test case for mib_resources_users_get_user_by_email


        """
        body = User()
        body.birthdate = "2020-01-01T00:00:00+00:00"
        body.email = "getuseremail@gm.com"
        body.firstname = "gg"
        body.lastname = "gg"
        body.password = "password"
        response = self.client.open(
            '/users',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        response = self.client.open(
            '/user_email/{user_email}'.format(user_email=body.email),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        response = self.client.open(
            '/user_email/{user_email}'.format(
                user_email="notexisting@gmail.com"),
            method='GET')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mib_resources_users_delete_user(self):
        """Test case for mib_resources_users_delete_user


        """
        response = self.client.open(
            '/users/{user_id}'.format(user_id=1),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        response = self.client.open(
            '/users/{user_id}'.format(user_id=345),
            method='DELETE')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_mib_resources_users_get_all_user(self):
        """Test case for mib_resources_users_get_all_user


        """
        response = self.client.open(
            '/users',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertIn("fake@gm.com", response.data.decode('utf-8'))

    def test_mib_resources_users_get_blacklist(self):
        """Test case for mib_resources_users_get_blacklist


        """
        response = self.client.open(
            '/users/{user_id}/blacklist'.format(user_id=1),
            method='GET')
        self.assert_200(response,
                        'Response body is : ' + response.data.decode('utf-8'))

    def test_mib_resources_users_add_to_blacklist(self):
        """Test case for mib_resources_users_add_to_blacklist

        Add a new user to the blacklist
        """
        body = UserListitem()
        body.id = 5
        response = self.client.open(
            '/users/1/blacklist',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mib_resources_users_add_to_report(self):
        """Test case for mib_resources_users_add_to_report

        Report a user
        """
        body = UserListitem()
        body.id = 5
        response = self.client.open(
            '/users/{user_id}/report'.format(user_id=789),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mib_resources_users_get_report(self):
        """Test case for mib_resources_users_get_report


        """
        response = self.client.open(
            '/users/{user_id}/report'.format(user_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
