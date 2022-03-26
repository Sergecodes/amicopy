from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView

from .forms import UserCreationForm

account_activation_token = PasswordResetTokenGenerator()
User = get_user_model()


class UserCreate(CreateView):
	model = User
	form_class = UserCreationForm
	template_name = 'users/auth/register.html'
	success_url = '/'

	def get(self, request, *args, **kwargs):
		"""
		Prevent currently logged in users from calling the register method without logging out.
		i.e Redirect them to index page.
		Only unauthed users can access this method..
		"""
		if request.user.is_authenticated:
			return redirect('/')

		return super().get(request, *args, **kwargs)

	def form_valid(self, form):
		# This method is called when the form has been successfully validated
		# also accounts for sending confirmation email to user.
		
		# Remember, by default, `is_active` field on User model is False
		# so user won't be permitted to log in, even though his record exists in db
		request, new_user = self.request, form.save()
		
		# compose and send email verification mail
		mail_subject = _('Activate your account')
		message = render_to_string('users/auth/email_confirm.html', {
			'user': new_user,
			'domain': get_current_site(request).domain,
			'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
			'token': account_activation_token.make_token(new_user)
		})
		to_email = new_user.email
		send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
	

		return HttpResponse(
			_(
				'Please confirm your email address to complete the registration.'
				'You should receive a confirmation email anytime soon.'
			)
		)


def activate_account(request, uidb64, token):
	"""Activate user account from email confirmation link"""
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	
	if user is not None and account_activation_token.check_token(user, token):
		# since phone number is ok, register user.
		user.is_active = True
		user.save()

		login_url = reverse('users:login')

        # TODO use custom html page instead
		return HttpResponse(
			_(
				'You have successfully confirmed your email. Now you can log into your account. <br>'
				'Login <a href="{}">here</a>.'.format(login_url)
			)
		)
	else:
        # TODO use custom htmo page instead
		signup_url = reverse('users:register')
		return HttpResponse(
			_(
				'Activation link is invalid. <br>'
				'Please <a href="{}">sign up</a> again in order to get a new link.'.format(signup_url)
			)
		)


