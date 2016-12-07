from django import template
import urllib, hashlib
register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.filter
def in_history(movie, user):
    exists = user.history.filter(movie=movie)
    if exists:
        return True
    return False

@register.filter
def in_watchlist(movie, user):
    exists = user.watchlist.filter(movie=movie)
    if exists:
        return True
    return False

@register.filter
def in_blocklist(movie, user):
    exists = user.blocklist.filter(movie=movie)
    if exists:
        return True
    return False

@register.filter
def is_important(movie, user):
    w = user.watchlist.filter(movie=movie)
    if w and w[0].important:
        return True
    return False

@register.simple_tag
def user_avatar(user):
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(user.email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':'retro', 's':str(100)}) # identicon
    return gravatar_url

@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, basestring):
        return text.startswith(starts)
    return False
