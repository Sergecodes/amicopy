from django.http import HttpResponseBadRequest
from functools import wraps


def require_ajax(view):
    """Imposes that a view is an ajax view"""

    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if request.is_ajax():
            return view(request, *args, **kwargs)
        else:
            raise HttpResponseBadRequest()
    return _wrapped_view

