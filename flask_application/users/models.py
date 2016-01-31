from flask.ext.security import UserMixin, RoleMixin

from flask_application.models import db, FlaskDocument


class Role(FlaskDocument, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class Profile(db.EmbeddedDocument):
    name = db.StringField(max_length=64)
    description = db.StringField(max_length=255)
    images = db.ListField(db.StringField(max_length=512), default=[])


class User(FlaskDocument, UserMixin):
    email = db.StringField(max_length=255)
    username = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    profiles = db.ListField(db.EmbeddedDocumentField('Profile'), default=[])


