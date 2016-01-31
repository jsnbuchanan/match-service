import datetime

from flask import Blueprint, current_app

from flask_application.controllers import TemplateView
from flask_application.users.models import User

public = Blueprint('public', __name__)


class IndexView(TemplateView):
    blueprint = public
    route = '/'
    route_name = 'home'
    template_name = 'home/index.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'now': datetime.datetime.now(),
            'config': current_app.config
        }


class ResultsView(TemplateView):
    blueprint = public
    route = '/results'
    route_name = 'results'
    template_name = 'home/results.html'

    def get_context_data(self, *args, **kwargs):
        users_with_profiles = User.objects.filter(__raw__={'$where': 'this.profiles.length >= 1'})
        profiles = []
        for user in users_with_profiles:
            for profile in user.profiles:
                profiles.append(profile)
        return {
            'profiles': profiles
        }
