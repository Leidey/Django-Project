from django.shortcuts import render

# Create your views here.

from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView
from django.views.generic import TemplateView


class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'user_registration.html'

    def get_success_url(self):
        return reverse('registered')
