# coding: utf-8

from __future__ import absolute_import
import json
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
            data=json.dumps(body.to_dict()),
            content_type='application/json')
        self.assertStatus(response, 201,
                          'Response body is : ' + response.data.decode('utf-8'))

        auth = AuthenticateBody()
        auth.email = body.email
        auth.password = body.password

        response = self.client.open(
            '/authenticate',
            method='POST',
            data=json.dumps(auth.to_dict()),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertIn(b"prova", response.data)

        auth.password = "1234"
        response = self.client.open(
            '/authenticate',
            method='POST',
            data=json.dumps(auth.to_dict()),
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
            data=json.dumps(body.to_dict()),
            content_type='application/json')
        self.assertStatus(response, 201,
                          'Response body is : ' + response.data.decode('utf-8'))
        self.assertIn("fake@gm.com", response.data.decode('utf-8'))

        # retry to create a user with same mail
        response = self.client.open(
            '/users',
            method='POST',
            data=json.dumps(body.to_dict()),
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

    def test_mib_resources_users_update_user(self):
        body = User()
        body.birthdate = "2020-01-01T00:00:00+00:00"
        body.email = "update@gm.com"
        body.firstname = "gg"
        body.lastname = "gg"
        body.password = "password"
        response = self.client.open(
            '/users',
            method='POST',
            data=json.dumps(body.to_dict()),
            content_type='application/json')
        self.assertStatus(response, 201,
                          'Response body is : ' + response.data.decode('utf-8'))
        self.assertIn("update@gm.com", response.data.decode('utf-8'))
        id_user = json.loads(response.data.decode('utf-8'))['id']
        body.email = "update2@gm.com"
        response = self.client.open(
            '/users/{user_id}'.format(user_id=id_user),
            data=json.dumps(body.to_dict()),
            method='PUT',
            content_type='application/json')
        self.assert200(response, "response is: "+response.data.decode('utf-8'))

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
            data=json.dumps(body.to_dict()),
            content_type='application/json')
        self.assertStatus(response, 201,
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

    def test_mib_resources_users_get_all_user(self):
        """Test case for mib_resources_users_get_all_user


        """
        response = self.client.open(
            '/users',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertIn("fake@gm.com", response.data.decode('utf-8'))

    def test_mib_resources_users_add_to_blacklist(self):
        """Test case for mib_resources_users_add_to_blacklist

        Add a new user to the blacklist
        """
        user1 = User()
        user1.birthdate = "2020-01-01T00:00:00+00:00"
        user1.email = "user1@gm.com"
        user1.firstname = "gg"
        user1.lastname = "gg"
        user1.password = "1234ABCD"
        response1 = self.client.open(
            '/users',
            method='POST',
            data=json.dumps(user1.to_dict()),
            content_type='application/json')
        self.assertStatus(response1, 201,
                          'Response body is : ' + response1.data.decode('utf-8'))

        user2 = User()
        user2.birthdate = "2020-01-01T00:00:00+00:00"
        user2.email = "user2@gm.com"
        user2.firstname = "gg"
        user2.lastname = "gg"
        user2.password = "1234ABCD"
        response2 = self.client.open(
            '/users',
            method='POST',
            data=json.dumps(user2.to_dict()),
            content_type='application/json')
        self.assertStatus(response2, 201,
                          'Response body is : ' + response2.data.decode('utf-8'))

        id_user = json.loads(response1.data.decode('utf-8'))
        id_blacklisted = json.loads(response2.data.decode('utf-8'))

        body = UserListitem()
        body.id = id_blacklisted['id']
        response = self.client.open(
            '/users/{user_id}/blacklist'.format(
                user_id=id_user['id']),
            method='POST',
            data=json.dumps(body.to_dict()),
            content_type='application/json')
        assert response.status_code == 200

        body = UserListitem()
        body.id = 999
        response = self.client.open(
            '/users/{user_id}/blacklist'.format(
                user_id=id_user['id']),
            method='POST',
            data=json.dumps(body.to_dict()),
            content_type='application/json')
        assert response.status_code == 404

        response = self.client.open(
            '/users/{user_id}/blacklist'.format(user_id=id_user['id']),
            method='GET')
        self.assert_200(response,
                        'Response body is : ' + response.data.decode('utf-8'))

        response = self.client.open(
            '/users/{user_id}/blacklist'.format(user_id=999),
            method='GET')
        self.assert_404(response,
                        'Response body is : ' + response.data.decode('utf-8'))

    def test_mib_resources_users_add_to_report(self):
        """Test case for mib_resources_users_add_to_report

        Report a user
        """

        user1 = User()
        user1.birthdate = "2020-01-01T00:00:00+00:00"
        user1.email = "usr1@gm.com"
        user1.firstname = "gg"
        user1.lastname = "gg"
        user1.password = "1234ABCD"
        response1 = self.client.open(
            '/users',
            method='POST',
            data=json.dumps(user1.to_dict()),
            content_type='application/json')
        self.assertStatus(response1, 201,
                          'Response body is : ' + response1.data.decode('utf-8'))

        user2 = User()
        user2.birthdate = "2020-01-01T00:00:00+00:00"
        user2.email = "usr2@gm.com"
        user2.firstname = "gg"
        user2.lastname = "gg"
        user2.password = "1234ABCD"
        response2 = self.client.open(
            '/users',
            method='POST',
            data=json.dumps(user2.to_dict()),
            content_type='application/json')
        self.assertStatus(response2, 201,
                          'Response body is : ' + response2.data.decode('utf-8'))

        id_user = json.loads(response1.data.decode('utf-8'))
        id_reported = json.loads(response2.data.decode('utf-8'))

        body = UserListitem()
        body.id = id_reported['id']
        response = self.client.open(
            '/users/{user_id}/report'.format(
                user_id=id_user['id']),
            method='POST',
            data=json.dumps(body.to_dict()),
            content_type='application/json')
        assert response.status_code == 200

        body = UserListitem()
        body.id = 999
        response = self.client.open(
            '/users/{user_id}/report'.format(
                user_id=id_user['id']),
            method='POST',
            data=json.dumps(body.to_dict()),
            content_type='application/json')
        assert response.status_code == 404

        response = self.client.open(
            '/users/{user_id}/report'.format(user_id=id_user['id']),
            method='GET')
        self.assert_200(response,
                        'Response body is : ' + response.data.decode('utf-8'))

        response = self.client.open(
            '/users/{user_id}/report'.format(user_id=999),
            method='GET')
        self.assert_404(response,
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
