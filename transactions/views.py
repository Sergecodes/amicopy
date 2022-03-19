from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from ipware import get_client_ip

from core.decorators import require_ajax
from .constants import AJAX_MESSAGE_TYPE
from .forms import SessionForm
from .models.models import Session, Device
from .utils import get_session_or_404


def test(request):
    return render(request, 'transactions/test.html')


class SessionCreate(CreateView):
    form_class = SessionForm
    model = Session
    template_name = 'transactions/session_create.html'

    def form_valid(self, form):
        request = self.request
        session, user = request.session, request.user
        session_obj = self.object = form.save(commit=False)

        ip, is_routable = get_client_ip(request)
        session_obj.creator_device = Device.objects.create(
            ip_address=ip, 
            display_name=request.POST['display_name'],
            browser_session_key=session._get_or_create_session_key(), 
            user=user if user.is_authenticated else None
        )

        session_obj.save()
        return redirect(session_obj)


class SessionDetail(DetailView):
    model = Session
    template_name = 'transactions/session_detail.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'


# Remember decorators are called top-bottom
@require_ajax
@require_GET
def verify_session_exists(request, uuid):
    found, result = get_session_or_404(uuid)

    if found:
        session = result
        return JsonResponse({
            'creator_code': session.creator_code,
            'title': session.title,
            'accepts_new_devices': session.accepts_new_devices
        })

    response = result
    return response


@require_ajax
@require_GET
def verify_creator_code(request, uuid, code):
    found, result = get_session_or_404(uuid)

    if found:
        session = result
        creator_code = session.creator_code

        if not creator_code:
            return JsonResponse({
                'msg_type': AJAX_MESSAGE_TYPE.NO_CREATOR_CODE,
            })

        if creator_code != code:
            return JsonResponse({
                'msg_type': AJAX_MESSAGE_TYPE.INVALID_CREATOR_CODE
            })

    response = result
    return response


@require_ajax
@require_POST
@login_required
def toggle_allow_new_devices(request, uuid):
    found, result = get_session_or_404(uuid)
    if not found:
        return result
        
    session = result
    
    # User should be owner of session
    if request.user != session.creator:
        return JsonResponse({
            'msg_type': AJAX_MESSAGE_TYPE.NOT_PERMITTED
        }, status=403)

    if session.accepts_new_devices:
        session.block_new_devices()
    else:
        session.allow_new_devices()

    return JsonResponse()

