from flask import current_app

from flask.ext.script import Command
from flask.ext.security.confirmable import confirm_user

from flask_application.models import FlaskDocument
from flask_application.users.models import Profile


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
        for u in (('Ian', 'hapgilmore23@gmail.com', 'password', ['admin'], True,
                   [Profile(name='Ian',
                            description='wickedly smart beneficent mastermind',
                            images=['img/profiles-samples/ian-fire.jpg',
                                     'img/profiles-samples/ian-frog.jpg',
                                     'img/profiles-samples/ian-color.jpg',
                                     'img/profiles-samples/ian-suckers.jpg'])]),
                  ('Christina', 'christina.cloward@gmail.com', 'password', ['editor'], True,
                   [Profile(name='Christina',
                           description='sexy funny kitty wrangler',
                           images=['img/profiles-samples/christina.jpg',
                                   'img/profiles-samples/gilmores.jpg',
                                   'img/profiles-samples/kitties.jpg'])]),
                  ('Jason', 'jsnbuchanan@gmail.com', 'password', ['admin'], True,
                   [Profile(name='Jason',
                           description='robust healthy male',
                           images=['img/profiles-samples/jason-potion.jpg',
                                   'img/profiles-samples/jason-warlord.jpg',
                                   'img/profiles-samples/jason-butt.jpg'])]),
                  ('Amy', 'aobuchanan@gmail.com', 'password', ['author'], True,
                   [Profile(name='Amy',
                            description='amazon warrior princess',
                            images=['img/profiles-samples/amy-kiss.jpg',
                                    'img/profiles-samples/amy-wifi.jpg',
                                    'img/profiles-samples/amy-savanah.jpg'])]),
                  ('Regular User', 'jsnbuchanan+noPerms@gmail.com', 'password', [], True, []),
                  ('Disabled User', 'jsnbuchanan+disabled@gmail.com', 'password', [], False, [])):
            user = current_app.user_datastore.create_user(
                username=u[0],
                email=u[1],
                password=u[2],
                roles=u[3],
                active=u[4],
                profiles=u[5]
            )
            confirm_user(user)

            current_app.user_datastore.commit()
