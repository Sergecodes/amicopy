from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class UsernameValidator(RegexValidator):
	"""
	Username rules:
	- Username should be between 1 to 50 characters.
	- Username should not contain any symbols, or spaces.
	- All other characters are allowed(letters, numbers, hyphens, and underscores).
	"""
    
	regex = r'\A[a-zA-Z0-9-_]{1,50}\Z'
	message = _(
		'Enter a valid username. This value should contain at most 50 characters. \n '
		'It should not contain any symbols or spaces; '
		'all other characters are allowed(letters, numbers, hyphens, and underscores)'
	)
	flags = 0

