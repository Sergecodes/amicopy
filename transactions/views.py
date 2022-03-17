from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from ipware import get_client_ip

from core.decorators import require_ajax
from .forms import SessionForm
from .models.models import Session, Device


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
            browser_session_id=session._get_or_create_session_key(), 
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
    try:
        session = Session.objects.get(uuid=uuid, is_active=True)
        return JsonResponse({
            'creator_code': session.creator_code,
            'title': session.title,
            'accepts_new_devices': session.accepts_new_devices
        })
    except Session.DoesNotExist:
        return JsonResponse({
            'message': _('No session found with this code'),
        }, status=404)


@require_ajax
@require_POST
@login_required
def allow_new_devices(request, session_uuid):
    try:
        session = Session.objects.get(uuid=session_uuid, is_active=True)
    except Session.DoesNotExist:
        return JsonResponse({
            'message': _('No active session found with this code'),
        }, status=404)

    # User should be owner of session
    if request.user != session.creator:
        return JsonResponse({
            'message': _('Not permitted')
        }, status=403)

    session.allow_new_devices()
    return JsonResponse()


@require_ajax
@require_POST
@login_required
def block_new_devices(request, session_uuid):
    try:
        session = Session.objects.get(uuid=session_uuid, is_active=True)
    except Session.DoesNotExist:
        return JsonResponse({
            'message': _('No active session found with this code'),
        }, status=404)

    # User should be owner of session
    if request.user != session.creator:
        return JsonResponse({
            'message': _('Not permitted')
        }, status=403)

    session.block_new_devices()
    return JsonResponse()
