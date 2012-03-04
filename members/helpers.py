#-*- coding: utf-8 -*-
import calendar
from datetime import date

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


def get_next_yearly_event(event_date, reference_date=date.today()):
    if event_date is None or reference_date is None:
        return None

    y = reference_date.year

    if event_date.month == 2 and event_date.day == 29:
        while True:
            while not calendar.isleap(y):
                y += 1
            next_leap = date(y, event_date.month, event_date.day)
            if next_leap >= reference_date:
                return next_leap
            else:
                y += 1

    next_event = date(y, event_date.month, event_date.day)
    if next_event < reference_date:
        return next_event.replace(year=reference_date.year + 1)
    else:
        return next_event


def days_until(event_date, reference_date=date.today()):
    """ counting days between dates """
    if event_date is None or reference_date is None:
        return None

    return abs(event_date - reference_date).days


def years_since(event_date, reference_date=date.today()):
    """ counting years between dates """
    if event_date is None or reference_date is None:
        return None

    years = reference_date.year - event_date.year
    if event_date.month < reference_date.month or event_date.month == reference_date.month and event_date.day <= reference_date.day:
        return years
    else:
        return years - 1
