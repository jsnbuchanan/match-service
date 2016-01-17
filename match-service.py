import werkzeug.exceptions as ex
from flask import Flask, render_template, abort
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask_mail import Mail

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'sometimes I make mistakes when choosing new frameworks'

#app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_TRACKABLE'] = True

app.config['MONGODB_DB'] = 'matchdatabase'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017
db = MongoEngine(app)

# app.config['MAIL_SERVER'] = 'localhost'
# app.config['MAIL_PORT'] = 25
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'username'
# app.config['MAIL_PASSWORD'] = 'password'
mail = Mail(app)

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    last_login_at = db.DateTimeField()
    current_login_at = db.DateTimeField()
    last_login_ip = db.StringField(max_length=45)
    current_login_ip = db.StringField(max_length=45)
    login_count = db.IntField()
    roles = db.ListField(db.ReferenceField(Role), default=[])


# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    user_datastore.create_user(email='jsnbuchanan@gmail.com', password='password')

# Static data model

christina = {'name':'Christina',
                       'description':'sexy funny kitty wrangler',
                       'images':['img/profiles-samples/christina.jpg',
                                 'img/profiles-samples/gilmores.jpg',
                                 'img/profiles-samples/kitties.jpg']}

jason = {'name':'Jason','description':'robust healthy male',
         # 'images':['img/profiles-samples/jason-potion.jpg',
         #           'img/profiles-samples/jason-warlord.jpg',
         #           'img/profiles-samples/jason-butt.jpg']
         }

ian = {'name':'Ian','description':'wickedly smart beneficent mastermind',
       'images':['img/profiles-samples/ian-fire.jpg',
                 'img/profiles-samples/ian-frog.jpg',
                 'img/profiles-samples/ian-color.jpg',
                 'img/profiles-samples/ian-suckers.jpg']
      }
amy = {'name':'Amy','description':'amazon warrior princess',
       'images':['img/profiles-samples/amy-kiss.jpg',
                 'img/profiles-samples/amy-wifi.jpg',
                 'img/profiles-samples/amy-savanah.jpg']
      }

match_profiles = {'profiles':[christina, ian, jason, amy]}


# Mapping Views and Routes
@app.route('/')
@app.route('/search/')
def home():
    return render_template('search.html')


@app.route('/profiles/')
@login_required
def profiles(request):
    return render_template("profiles.html", profile=christina)


@app.route('/profile/<profile_name>/')
def profile(profile_name="Christina"):
    for profile_x in match_profiles['profiles']:
        if profile_x['name'] == profile_name:
            selected_profile = profile_x
    try:
        selected_profile
    except NameError:
        abort(404)
    return render_template("profile.html", profile=selected_profile)


@app.route('/results/')
def results():
    for profile_x in match_profiles['profiles']:
        if 'images' not in profile_x.keys():
            profile_x['images'] = ['img/profile.jpg']
    return render_template("results.html", profiles=match_profiles['profiles'])


@app.errorhandler(404)
def profile_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
