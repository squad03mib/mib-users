from os import stat
from swagger_server.dao.manager import Manager
from swagger_server.models_db.user import User
from swagger_server.models_db.blacklist import Blacklist


class UserManager(Manager):

    @staticmethod
    def create_user(user: User):
        Manager.create(user=user)

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return User.query.get(id_)

    @staticmethod
    def retrieve_by_email(email):
        Manager.check_none(email=email)
        return User.query.filter(User.email == email).first()

    @staticmethod
    def update_user(user: User):
        Manager.update(user=user)

    @staticmethod
    def delete_user(user: User):
        Manager.delete(user=user)

    @staticmethod
    def delete_user_by_id(id_: int):
        user = UserManager.retrieve_by_id(id_)
        UserManager.delete_user(user)

    @staticmethod
    def list_active_users():
        users = User.query.filter(User.is_active.is_(True)).all()
        return users

    @staticmethod
    def create_blacklist(blacklist: Blacklist):
        Manager.create(blacklist=blacklist)

    @staticmethod
    def retrieve_blacklist(id_user_: int):
        return Blacklist.query.filter(Blacklist.id_user == id_user_).all()

    @staticmethod
    def retrieve_blacklisted_user(id_user, id_blacklisted):
        return Blacklist.query.filter(Blacklist.id_user == id_user).filter(Blacklist.id_blacklisted == id_blacklisted).first()

    @staticmethod
    def update_blacklist(blacklist: Blacklist):
        Manager.update(blacklist=blacklist)

    @staticmethod
    def delete_blacklist(blacklist: Blacklist):
        Manager.delete(blacklist=blacklist)
