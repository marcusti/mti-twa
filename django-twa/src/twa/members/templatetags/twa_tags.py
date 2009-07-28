from PIL import Image
from django import template
from django.template.defaultfilters import stringfilter
import locale
import os

locale.setlocale( locale.LC_ALL, 'de_DE.UTF-8' )
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

def thumbnail( file, size = '64x64' ):
    # defining the size
    x, y = [int( x ) for x in size.split( 'x' )]
    # defining the filename and the miniature filename
    filehead, filetail = os.path.split( file.path )
    basename, format = os.path.splitext( filetail )
    miniature = basename + '_' + size + format
    filename = file.path
    miniature_filename = os.path.join( filehead, miniature )
    filehead, filetail = os.path.split( file.url )
    miniature_url = filehead + '/' + miniature
    if os.path.exists( miniature_filename ) and os.path.getmtime( filename ) > os.path.getmtime( miniature_filename ):
        os.unlink( miniature_filename )
    # if the image wasn't already resized, resize it
    if not os.path.exists( miniature_filename ):
        image = Image.open( filename )
        image.thumbnail( [x, y], Image.ANTIALIAS )
        try:
            image.save( miniature_filename, image.format, quality = 90, optimize = 1 )
        except:
            image.save( miniature_filename, image.format, quality = 90 )
    return miniature_url

register.filter( thumbnail )
register.inclusion_tag( 'paginator.html', takes_context = True )( paginator )
