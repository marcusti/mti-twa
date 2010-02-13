#-*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

DEFAULT_MAX_LENGTH = 200

class AbstractModel( models.Model ):
    public = models.BooleanField( _( u'Public' ), default = True, help_text = '' )
    created = models.DateTimeField( _( u'Created' ), auto_now_add = True, help_text = '' )
    last_modified = models.DateTimeField( _( u'Last Modified' ), auto_now = True, help_text = '' )

    class Meta:
        abstract = True
