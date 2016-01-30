from flask import current_app

from flask.ext.script import Command
from flask.ext.security.confirmable import confirm_user

from flask_application.models import FlaskDocument


class ResetDB(Command):
    """Drops all tables and recreates them"""
    def run(self, **kwargs):
        self.drop_collections()

    @staticmethod
    def drop_collections():
        for klass in FlaskDocument.all_subclasses():
            klass.drop_collection()


class PopulateDB(Command):
    """Fills in predefined data to DB"""
    def run(self, **kwargs):
        self.create_roles()
        self.create_users()

    @staticmethod
    def create_roles():
        for role in ('admin', 'editor', 'author'):
            current_app.user_datastore.create_role(name=role, description=role)
        current_app.user_datastore.commit()

    @staticmethod
    def create_users():
        for u in (('ian', 'hapgilmore23@gmail.com', 'password', ['admin'], True),
                  ('christina', 'christina.cloward@gmail.com', 'password', ['editor'], True),
                  ('jason', 'jsnbuchanan@gmail.com', 'password', ['admin'], True),
                  ('amy', 'aobuchanan@gmail.com', 'password', ['author'], False)):
            user = current_app.user_datastore.create_user(
                username=u[0],
                email=u[1],
                password=u[2],
                roles=u[3],
                active=u[4]
            )
            confirm_user(user)

            current_app.user_datastore.commit()
