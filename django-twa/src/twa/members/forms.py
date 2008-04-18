#-*- coding: utf-8 -*-

from django import newforms as forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from twa.members.models import DEFAULT_MAX_LENGTH

class LoginForm( forms.Form ):
    username = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
                                min_length = 4,
                                label = _( 'Username' ),
                                required = True,
                                error_messages = {'required': _( 'Username is required.' ),
                                                  'min_length': _( 'Username is too short.' ),
                                                  },
                                )
    password = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
                                min_length = 4,
                                label = _( 'Password' ),
                                required = True,
                                widget = forms.PasswordInput,
                                error_messages = {'required': _( 'Password is required.' ),
                                                  'min_length': _( 'Passord is too short.' ),
                                                  },
                                )
#    next = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
#                            required = False,
#                            widget = forms.HiddenInput,
#                            )

    def clean( self ):
        username = self.data['username']
        password = self.data['password']

        self.user = authenticate( username = username, password = password )

        if self.user is None:
            raise forms.ValidationError, _( 'Please enter a correct username and password. Note that both fields are case-sensitive.' )

        elif not self.user.is_active:
            raise forms.ValidationError, _( 'This account is inactive.' )

        return super( LoginForm, self ).clean()

    def get_user( self ):
        return self.user
