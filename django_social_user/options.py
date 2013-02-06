from django.conf import settings

# setup option constants
KEY_ACCESS_TOKEN_FAILURE = 'REDIRECT_ON_ACCESS_TOKEN_FAILURE'
KEY_AUTHENTICATION = 'REDIRECT_ON_AUTHENTICATION'
KEY_DATA_DICT = 'DJANGO_SOCIAL_USER_OPTIONS'
KEY_REQUEST_TOKEN_FAILURE = 'REDIRECT_ON_REQUEST_TOKEN_FAILURE'

# setup legacy options constants
LEGACY_PREFIX = 'SOCIAL_USER_%s'
LEGACY_REDIRECT_ON_ACCESS_TOKEN_FAILURE = (
    LEGACY_PREFIX % KEY_ACCESS_TOKEN_FAILURE)
LEGACY_REDIRECT_ON_AUTHENTICATION = LEGACY_PREFIX % KEY_AUTHENTICATION
LEGACY_REDIRECT_ON_REQUEST_TOKEN_FAILURE = (
    LEGACY_PREFIX % KEY_REQUEST_TOKEN_FAILURE)

# find the configuration objects from the settings.py
opts = getattr(settings, KEY_DATA_DICT, None) or {}

# if the user should be redirected to an error page on access token failure,
#   then define that redirect here, otherwise a 404 will be raised
#   won't know where to redirect to.
REDIRECT_ON_ACCESS_TOKEN_FAILURE = (
    opts.get(KEY_ACCESS_TOKEN_FAILURE) or
    getattr(settings, LEGACY_REDIRECT_ON_ACCESS_TOKEN_FAILURE, ''))

# this should be defined, if users should always be redirected to the
#   same page after authenticating. If either this value or the 'next' session
#   variable are not defined, then a 404 will be raised, because library
#   won't know where to redirect to.
REDIRECT_ON_AUTHENTICATION = (
    opts.get(KEY_AUTHENTICATION) or
    getattr(settings, LEGACY_REDIRECT_ON_AUTHENTICATION, ''))

# if the user should be redirected to an error page on request token failure,
#   then define that redirect here, otherwise a 404 will be raised
REDIRECT_ON_REQUEST_TOKEN_FAILURE = (
    opts.get(KEY_REQUEST_TOKEN_FAILURE) or
    getattr(settings, LEGACY_REDIRECT_ON_REQUEST_TOKEN_FAILURE, ''))
