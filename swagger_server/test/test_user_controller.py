# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.authenticate_body import AuthenticateBody  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.inline_response_default import InlineResponseDefault  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_listitem import UserListitem  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_mib_resources_auth_authenticate(self):
        """Test case for mib_resources_auth_authenticate

        Authenticate a user
        """
        body = AuthenticateBody()
        body.email = "helo@helo.com"
        body.password = "2"

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

    def test_mib_resources_users_create_user(self):
        """Test case for mib_resources_users_create_user

        Add a new user
        """
        body = User()
        body.birthdate = "2020-01-01T00:00:00+00:00"
        body.email = "fake@gm.com"
        body.firstname = "gg"
        body.lastname = "gg"
        body.password = "succhiamelo"
        response = self.client.open(
            '/users',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mib_resources_users_delete_user(self):
        """Test case for mib_resources_users_delete_user


        """
        response = self.client.open(
            '/users/{user_id}'.format(user_id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mib_resources_users_get_all_user(self):
        """Test case for mib_resources_users_get_all_user

        
        """
        response = self.client.open(
            '/users',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mib_resources_users_get_blacklist(self):
        """Test case for mib_resources_users_get_blacklist

        
        """
        response = self.client.open(
            '/users/{user_id}/blacklist'.format(user_id=789),
            method='GET')
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

    def test_mib_resources_users_get_user(self):
        """Test case for mib_resources_users_get_user

        
        """
        response = self.client.open(
            '/users/{user_id}'.format(user_id=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_mib_resources_users_get_user_by_email(self):
        """Test case for mib_resources_users_get_user_by_email

        
        """
        response = self.client.open(
            '/user_email/{user_email}'.format(user_email='user_email_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
