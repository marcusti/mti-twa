#-*- coding: utf-8 -*-
from django.contrib.markup.templatetags.markup import markdown, restructuredtext, textile
from django.template.defaultfilters import linebreaks, urlize


MARKUP_MARKDOWN = 'markdown'
MARKUP_REST = 'restructuredtext'
MARKUP_TEXT = 'text'
MARKUP_TEXTILE = 'textile'


def txt_to_html(text, markup=MARKUP_TEXT):
    if markup == MARKUP_MARKDOWN:
        html = markdown(text)
    elif markup == MARKUP_REST:
        html = restructuredtext(text)
    elif markup == MARKUP_TEXTILE:
        html = textile(text)
    else:
        html = linebreaks(urlize(text))

    return html
