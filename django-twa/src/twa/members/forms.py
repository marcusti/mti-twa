#-*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from twa.members.models import *

DATE_INPUT_FORMATS = ['%Y-%m-%d', '%y-%m-%d', '%d.%m.%Y', '%d.%m.%y']
DATE_HELP_TEXT_FORMATS = 'dd.mm.yyyy, yyyy-mm-dd'

class TWAMembershipRequestForm( forms.Form ):
    firstname = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
                                 min_length = 2,
                                 label = _( 'First Name' ),
                                 required = True,
                                 error_messages = {'required': _( 'Firstname is required.' ),
                                                   'min_length': _( 'Firstname is too short.' ),
                                                   },
                                 )
    lastname = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
                                min_length = 2,
                                label = _( 'Last Name' ),
                                required = True,
                                error_messages = {'required': _( 'Lastname is required.' ),
                                                  'min_length': _( 'Lastname is too short.' ),
                                                  },
                                )
    street = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
                              min_length = 2,
                              label = _( 'Street' ),
                              required = True,
                              error_messages = {'required': _( 'Street is required.' ),
                                                'min_length': _( 'Street is too short.' ),
                                                },
                              )
    zip = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
                           min_length = 4,
                           label = _( 'Zip' ),
                           required = True,
                           error_messages = {'required': _( 'Zip is required.' ),
                                             'min_length': _( 'Zip is too short.' ),
                                             },
                           )
    city = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
                            min_length = 2,
                            label = _( 'City' ),
                            required = True,
                            error_messages = {'required': _( 'City is required.' ),
                                              'min_length': _( 'City is too short.' ),
                                              },
                            )
    country = forms.ChoiceField( choices = Country.objects.values_list('id', 'name'),
                                 initial = 1, # Germany
                                 label = _( 'Country' ),
                                 required = True,
                                 error_messages = {'required': _( 'Country is required.' ),
                                                   'invalid_choice': _( 'Please choose a valid country.' ),
                                                   },
                                 )
    phone = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
                             min_length = 4,
                             label = _( 'Phone' ),
                             required = False,
                             error_messages = {'required': _( 'Phone is required.' ),
                                               'min_length': _( 'Phone is too short.' ),
                                               },
                             )
    fax = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
                           min_length = 4,
                           label = _( 'Fax' ),
                           required = False,
                           error_messages = {'required': _( 'Fax is required.' ),
                                             'min_length': _( 'Fax is too short.' ),
                                             },
                           )
    mobile = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
                              min_length = 4,
                              label = _( 'Mobile' ),
                              required = False,
                              error_messages = {'required': _( 'Mobile is required.' ),
                                                'min_length': _( 'Mobile is too short.' ),
                                                },
                              )
    email = forms.EmailField( max_length = DEFAULT_MAX_LENGTH,
                              min_length = 4,
                              label = _( 'Email' ),
                              required = False,
                              error_messages = {'required': _( 'Email is required.' ),
                                                'min_length': _( 'Email is too short.' ),
                                                'invalid': _( 'Please enter a valid email address.' ),
                                                },
                              )
    birth = forms.DateField( label = _( 'Birth' ),
                             required = True,
                             widget = forms.DateTimeInput,
                             input_formats = DATE_INPUT_FORMATS,
                             error_messages = {'required': _( 'Birthday is required.' ),
                                               'invalid': _( 'Please enter a valid date. Valid formats are %s.' % DATE_HELP_TEXT_FORMATS ),
                                               },
                             )
    aikido = forms.DateField( label = _( 'Aikido since' ),
                              required = True,
                              input_formats = DATE_INPUT_FORMATS,
                              error_messages = {'required': _( '"Aikido since" is required.' ),
                                                'invalid': _( 'Please enter a valid date. Valid formats are %s.' % DATE_HELP_TEXT_FORMATS ),
                                                },
                              )
    kyu5 = forms.DateField( label = _( '5. Kyu' ),
                            required = False,
                            input_formats = DATE_INPUT_FORMATS,
                            error_messages = {'required': _( '5. Kyu is required.' ),
                                              'invalid': _( 'Please enter a valid date. Valid formats are %s.' % DATE_HELP_TEXT_FORMATS ),
                                              },
                            )
    kyu4 = forms.DateField( label = _( '4. Kyu' ),
                            required = False,
                            input_formats = DATE_INPUT_FORMATS,
                            error_messages = {'required': _( '4. Kyu is required.' ),
                                              'invalid': _( 'Please enter a valid date. Valid formats are %s.' % DATE_HELP_TEXT_FORMATS ),
                                              },
                            )
    kyu3 = forms.DateField( label = _( '3. Kyu' ),
                            required = False,
                            input_formats = DATE_INPUT_FORMATS,
                            error_messages = {'required': _( '3. Kyu is required.' ),
                                              'invalid': _( 'Please enter a valid date. Valid formats are %s.' % DATE_HELP_TEXT_FORMATS ),
                                              },
                            )
    kyu2 = forms.DateField( label = _( '2. Kyu' ),
                            required = False,
                            input_formats = DATE_INPUT_FORMATS,
                            error_messages = {'required': _( '2.Kyu is required.' ),
                                              'invalid': _( 'Please enter a valid date. Valid formats are %s.' % DATE_HELP_TEXT_FORMATS ),
                                              },
                            )
    kyu1 = forms.DateField( label = _( '1. Kyu' ),
                            required = False,
                            input_formats = DATE_INPUT_FORMATS,
                            error_messages = {'required': _( '1.Kyu is required.' ),
                                              'invalid': _( 'Please enter a valid date. Valid formats are %s.' % DATE_HELP_TEXT_FORMATS ),
                                              },
                            )
    dan1 = forms.DateField( label = _( '1. Dan' ),
                            required = False,
                            input_formats = DATE_INPUT_FORMATS,
                            error_messages = {'required': _( '1.Dan is required.' ),
                                              'invalid': _( 'Please enter a valid date. Valid formats are %s.' % DATE_HELP_TEXT_FORMATS ),
                                              },
                            )
    dan2 = forms.DateField( label = _( '2. Dan' ),
                            required = False,
                            input_formats = DATE_INPUT_FORMATS,
                            error_messages = {'required': _( '2.Dan is required.' ),
                                              'invalid': _( 'Please enter a valid date. Valid formats are %s.' % DATE_HELP_TEXT_FORMATS ),
                                              },
                            )
    dan3 = forms.DateField( label = _( '3. Dan' ),
                            required = False,
                            input_formats = DATE_INPUT_FORMATS,
                            error_messages = {'required': _( '3.Dan is required.' ),
                                              'invalid': _( 'Please enter a valid date. Valid formats are %s.' % DATE_HELP_TEXT_FORMATS ),
                                              },
                            )
    dan4 = forms.DateField( label = _( '4. Dan' ),
                            required = False,
                            input_formats = DATE_INPUT_FORMATS,
                            error_messages = {'required': _( '4.Dan is required.' ),
                                              'invalid': _( 'Please enter a valid date. Valid formats are %s.' % DATE_HELP_TEXT_FORMATS ),
                                              },
                            )
    dan5 = forms.DateField( label = _( '5. Dan' ),
                            required = False,
                            input_formats = DATE_INPUT_FORMATS,
                            error_messages = {'required': _( '5.Dan is required.' ),
                                              'invalid': _( 'Please enter a valid date. Valid formats are %s.' % DATE_HELP_TEXT_FORMATS ),
                                              },
                            )
    photo = forms.FileField( label = _( 'Photo' ),
                              required = False,
                              error_messages = {'required': _( 'Photo is required.' ),
                                                'missing': _( 'Photo is missing.' ),
                                                'empty': _( 'Photo is empty.' ),
                                                'min_length': _( 'Photo is too short.' ),
                                                },
                              )

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
