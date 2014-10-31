from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import SteamUser

class UsernameForm(forms.ModelForm):

    class Meta:
        model = SteamUser
        fields = ('nickname',)
        labels = {
            'nickname': _('Input your Steam username'),
        }