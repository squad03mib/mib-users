from typing import List
import connexion
from swagger_server.models.authenticate_body import AuthenticateBody  # noqa: E501
from swagger_server.models.inline_response_default import InlineResponseDefault  # noqa: E501
from swagger_server.models_db.user import User  # noqa: E501
from swagger_server.models_db.blacklist import Blacklist
from swagger_server.models_db.report import Report
from swagger_server.models.user import User as UserSchema
from swagger_server.models.user_listitem import UserListitem  # noqa: E501
from swagger_server import util
from swagger_server.dao.user_manager import UserManager
from flask import jsonify, Response, abort

NUM_REPORTS = 2


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

    return jsonify(response), status_code


def mib_resources_users_update_user(user_id, body):  # noqa: E501
    if connexion.request.is_json:
        body = UserSchema.from_dict(connexion.request.get_json())  # noqa: E501
    user = UserManager.retrieve_by_id(user_id)
    if user is not None:
        user.set_email(body.email)
        user.set_password(body.password)
        user.set_first_name(body.firstname)
        user.set_last_name(body.lastname)
        UserManager.update_user(user)


def mib_resources_users_create_user(body):  # noqa: E501
    """Add a new user

     # noqa: E501

    :param body: Create a new customer inside microservice app
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = UserSchema.from_dict(connexion.request.get_json())  # noqa: E501

    if UserManager.retrieve_by_email(body.email) is not None:
        return Response(status=403)

    user = User()
    user.set_email(body.email)
    user.set_password(body.password)
    user.set_first_name(body.firstname)
    user.set_last_name(body.lastname)
    UserManager.create_user(user)

    return user.serialize(), 201


def mib_resources_users_delete_user(user_id):  # noqa: E501
    """mib_resources_users_delete_user

    Delete a user by its id # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: None
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is not None:
        user.is_active = False
        UserManager.update_user(user)
        return Response(status=200)

    return Response(status=404)


def mib_resources_users_get_all_user():  # noqa: E501
    """mib_resources_users_get_all_user

    Get all users list # noqa: E501


    :rtype: List[UserListitem]
    """
    list = UserManager.list_active_users()

    return [user.serialize() for user in list]


def mib_resources_users_get_user(user_id):  # noqa: E501
    """mib_resources_users_get_user

    Get a user by its id # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: None
    """
    user = UserManager.retrieve_by_id(user_id)
    if user is not None:
        return user.serialize()
    return Response(status=404)


def mib_resources_users_get_user_by_email(user_email):  # noqa: E501
    """mib_resources_users_get_user_by_email

    Get a user by its email # noqa: E501

    :param user_email: User Unique Email
    :type user_email: str

    :rtype: None
    """
    user = UserManager.retrieve_by_email(user_email)
    if user is not None:
        return user.serialize()
    return {}, 404


def mib_resources_users_add_to_blacklist(body, user_id):  # noqa: E501
    """Add a new user to the blacklist

     # noqa: E501

    :param body: Add a new user to the blacklist
    :type body: dict | bytes
    :param user_id: User Unique ID
    :type user_id: int

    :rtype: None
    """

    if connexion.request.is_json:
        body = UserListitem.from_dict(connexion.request.get_json())  # noqa: E501

    if user_id == body.id:
        return abort(404)

    user = UserManager.retrieve_by_id(user_id)
    user_blacklisted = UserManager.retrieve_by_id(body.id)

    if user is None or user_blacklisted is None:
        return abort(404)

    list = UserManager.retrieve_blacklist(user_id)
    elem = UserManager.retrieve_blacklisted_user(
        user_id, body.id)

    if list is [] or elem is None:
        blacklist = Blacklist()
        blacklist.id_user = user_id
        blacklist.id_blacklisted = body.id
        UserManager.create_blacklist(blacklist)

    list = UserManager.retrieve_blacklist(user_id)

    return [item.serialize() for item in list], 200


def mib_resources_users_delete_user_from_blacklist(user_id, blacklisted_id):
    """mib_resources_users_delete_user_from_blacklist

    Delete a user from the blacklist # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int
    :param user_blacklisted_idid: User Unique ID
    :type blacklisted_id: int

    :rtype: None
    """
    if user_id == blacklisted_id:
        return abort(404)

    user = UserManager.retrieve_by_id(user_id)
    user_blacklisted = UserManager.retrieve_by_id(blacklisted_id)

    if user is None or user_blacklisted is None:
        return abort(404)

    blacklist = UserManager.retrieve_blacklisted_user(user_id, blacklisted_id)

    UserManager.delete_blacklist(blacklist)

    return Response(status=200)


def mib_resources_users_get_blacklist(user_id):  # noqa: E501
    """mib_resources_users_get_blacklist

    Get the blacklist of a user # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: List[UserListitem]
    """
    user = UserManager.retrieve_by_id(user_id)

    if user is None:
        return abort(404)

    blacklist = UserManager.retrieve_blacklist(user_id)

    return [item.serialize() for item in blacklist]


def mib_resources_users_add_to_report(body, user_id):  # noqa: E501
    """Report a user

     # noqa: E501

    :param body: Add a new user to the list of reported users
    :type body: dict | bytes
    :param user_id: User Unique ID
    :type user_id: int

    :rtype: None
    """

    if connexion.request.is_json:
        body = UserListitem.from_dict(connexion.request.get_json())  # noqa: E501

    if user_id == body.id:
        return abort(404)

    user = UserManager.retrieve_by_id(user_id)
    user_reported = UserManager.retrieve_by_id(body.id)

    if user is None or user_reported is None:
        return abort(404)

    list = UserManager.retrieve_report(user_id)
    elem = UserManager.retrieve_reported_user(
        user_id, body.id)

    if list is [] or elem is None:
        report = Report()
        report.id_user = user_id
        report.id_reported = body.id
        UserManager.create_report(report)

    num_reports = len(UserManager.retrieve_num_reports(user_reported))

    if num_reports == NUM_REPORTS:
        user_reported.set_is_reported()
        UserManager.update_user(user_reported)

    list = UserManager.retrieve_report(user_id)

    return [item.serialize() for item in list], 200


def mib_resources_users_get_report(user_id):  # noqa: E501
    """mib_resources_users_get_report

    Get the list of reported users # noqa: E501

    :param user_id: User Unique ID
    :type user_id: int

    :rtype: List[UserListitem]
    """
    user = UserManager.retrieve_by_id(user_id)

    if user is None:
        return abort(404)

    report = UserManager.retrieve_report(user_id)

    return [item.serialize() for item in report]
