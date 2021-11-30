import connexion
import six
import datetime

from swagger_server.models.authenticate_body import AuthenticateBody  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.inline_response_default import InlineResponseDefault  # noqa: E501
from swagger_server.models_db.user import User  # noqa: E501
from swagger_server.models.user import User as UserSchema
from swagger_server.models.user_listitem import UserListitem  # noqa: E501
from swagger_server import util
from swagger_server.dao.user_manager import UserManager


def mib_resources_auth_authenticate(body):  # noqa: E501
    """Authenticate a user

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        body = AuthenticateBody.from_dict(connexion.request.get_json())  # noqa: E501

    user = UserManager.retrieve_by_email(body.email)
    response = {
        'authentication': 'failure',
        'user': None
    }
    status_code = 401
    if user and user.authenticate(body.password):
        response['authentication'] = 'success'
        response['user'] = user.serialize()
        status_code = 200

    return Response(status=status_code, response=response)


def mib_resources_users_create_user(body):  # noqa: E501
    """Add a new user

     # noqa: E501

    :param body: Create a new customer inside microservice app
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = UserSchema.from_dict(connexion.request.get_json())  # noqa: E501

    user = User()
    user.set_email(body.email)
    user.set_password(body.password)
    user.set_first_name(body.firstname)
    user.set_last_name(body.lastname)
    UserManager.create_user(user)

    response_object = {
        'user': user.serialize(),
        'status': 'success',
        'message': 'Successfully registered',
    }

    return response_object


def mib_resources_users_delete_user(user_id):  # noqa: E501
    """mib_resources_users_delete_user

    Delete a user by its id # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: None
    """
    return 'do some magic!'


def mib_resources_users_get_all_user():  # noqa: E501
    """mib_resources_users_get_all_user

    Get all users list # noqa: E501


    :rtype: List[UserListitem]
    """
    return 'do some magic!'


def mib_resources_users_get_blacklist(user_id):  # noqa: E501
    """mib_resources_users_get_blacklist

    Get the blacklist of a user # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: List[UserListitem]
    """
    return 'do some magic!'


def mib_resources_users_get_report(user_id):  # noqa: E501
    """mib_resources_users_get_report

    Get the list of reported users # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: List[UserListitem]
    """
    return 'do some magic!'


def mib_resources_users_get_user(user_id):  # noqa: E501
    """mib_resources_users_get_user

    Get a user by its id # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: None
    """
    return UserManager.retrieve_by_id(user_id).serialize()


def mib_resources_users_get_user_by_email(user_email):  # noqa: E501
    """mib_resources_users_get_user_by_email

    Get a user by its email # noqa: E501

    :param user_email: User Unique Email
    :type user_email: str

    :rtype: None
    """
    return 'do some magic!'
