from django import template
from django.template.defaultfilters import stringfilter
import locale
import os

locale.setlocale( locale.LC_ALL, '' )
register = template.Library()

@register.simple_tag
def maximum( a1, a2 ):
    return max( a1, a2 )

@register.filter()
def num_format( value ):
    return locale.format( "%d", value, grouping = True )

@register.filter
@stringfilter
def extension( value ):
    try:
        root, ext = os.path.splitext( value )
        if ext and len( ext ) > 0:
            if ext.startswith( '.' ):
                return ext.lower()[1:]
            else:
                return ext.lower()
        return value
    except:
        return value

def paginator( context, adjacent_pages = 3 ):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    """
    page_numbers = [n for n in \
                    range( context['page'] - adjacent_pages, context['page'] + adjacent_pages + 1 ) \
                    if n > 0 and n <= context['pages']]
    return {
        'hits': context['hits'],
        'results_per_page': context['results_per_page'],
        'page': context['page'],
        'pages': context['pages'],
        'page_numbers': page_numbers,
        'next': context['next'],
        'previous': context['previous'],
        'has_next': context['has_next'],
        'has_previous': context['has_previous'],
        'show_first': 1 not in page_numbers,
        'show_last': context['pages'] not in page_numbers,
    }

register.inclusion_tag( 'paginator.html', takes_context = True )( paginator )
