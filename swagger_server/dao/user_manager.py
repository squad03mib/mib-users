from os import stat
from swagger_server.dao.manager import Manager
from swagger_server.models_db.user import User
from swagger_server.models_db.blacklist import Blacklist
from swagger_server.models_db.report import Report


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
        return User.query.filter(User.email == email).filter(User.is_reported.is_(False)).first()

    @staticmethod
    def update_user(user: User):
        Manager.update(user=user)

    @staticmethod
    def delete_user(user: User):
        Manager.delete(user=user)

    @staticmethod
    def list_active_users():
        users = User.query.filter(User.is_active.is_(True)).filter(
            User.is_reported.is_(False)).all()
        return users

    @staticmethod
    def create_blacklist(blacklist: Blacklist):
        Manager.create(blacklist=blacklist)

    @staticmethod
    def delete_blacklist(blacklist: Blacklist):
        Manager.delete(blacklist=blacklist)

    @staticmethod
    def retrieve_blacklist(id_user_: int):
        return Blacklist.query.filter(Blacklist.id_user == id_user_).all()

    @staticmethod
    def retrieve_blacklisted_user(id_user, id_blacklisted):
        return Blacklist.query.filter(Blacklist.id_user == id_user).filter(Blacklist.id_blacklisted == id_blacklisted).first()

    @staticmethod
    def create_report(report: Report):
        Manager.create(report=report)

    @staticmethod
    def retrieve_report(id_user_: int):
        return Report.query.filter(Report.id_user == id_user_).all()

    @staticmethod
    def retrieve_num_reports(id_user_: int):
        return Report.query.filter(Report.id_reported == id_user_).all()

    @staticmethod
    def retrieve_reported_user(id_user, id_reported):
        return Report.query.filter(Report.id_user == id_user).filter(Report.id_reported == id_reported).first()
