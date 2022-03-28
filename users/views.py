# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.contrib.auth.tokens import PasswordResetTokenGenerator 
# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import send_mail
# from django.http.response import HttpResponse
# from django.shortcuts import redirect
# from django.template.loader import render_to_string
# from django.urls import reverse
# from django.utils.encoding import force_bytes, force_str
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.translation import gettext_lazy as _
# from django.views.generic.edit import CreateView
# from rest_framework import status, generics
# from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .constants import API_MESSAGE_TYPE
# from .forms import UserCreationForm

# account_activation_token = PasswordResetTokenGenerator()
# User = get_user_model()


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def activate_account(request, uidb64, token):
# 	"""Activate user account from email confirmation link"""
# 	try:
# 		uid = force_str(urlsafe_base64_decode(uidb64))
# 		user = User.objects.get(pk=uid)
# 	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
# 		user = None
	
# 	if user is not None and account_activation_token.check_token(user, token):
# 		user.is_active = True
# 		user.save()

# 		return Response({'msg_type': API_MESSAGE_TYPE.EMAIL_CONFIRMED.value}, status=status.HTTP_200_OK)
# 	else:
# 		return Response({'msg_type': API_MESSAGE_TYPE.LINK_EXPIRED.value}, status=status.HTTP_400_BAD_REQUEST)


# class UserCreate(APIView):
# 	permission_classes = [AllowAny]

# 	def _form_valid(self, form):
# 		# This method is called when the form has been successfully validated
# 		# also accounts for sending confirmation email to user.
		
# 		# Remember, by default, `is_active` field on User model is False
# 		# so user won't be permitted to log in, even though his record exists in db
# 		request, new_user = self.request, form.save()
		
# 		# compose and send email verification mail
# 		mail_subject = _('Activate your account')
# 		message = render_to_string('users/auth/email_confirm.html', {
# 			'user': new_user,
# 			'domain': get_current_site(request).domain,
# 			'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
# 			'token': account_activation_token.make_token(new_user)
# 		})
# 		to_email = new_user.email
# 		send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])

# 		return Response({'msg_type': API_MESSAGE_TYPE.EMAIL_SENT.value}, status=status.HTTP_200_OK)

# 	def _form_invalid(self, form):
# 		return Response(form.errors.as_json(), status=status.HTTP_400_BAD_REQUEST)

# 	def post(self, request, format=None):
# 		form = UserCreationForm(request.data)
# 		if form.is_valid():
# 			return self._form_valid(form)
# 		else:
# 			return self._form_invalid(form)


# class UserUpdate(APIView):
# 	pass