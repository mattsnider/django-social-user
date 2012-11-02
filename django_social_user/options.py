from django.conf import settings

# if the user should be redirected to an error page on request token failure,
#   then define that redirect here, otherwise a 404 will be raised
SOCIAL_USER_REDIRECT_ON_REQUEST_TOKEN_FAILURE = getattr(settings,
    'SOCIAL_USER_REDIRECT_ON_REQUEST_TOKEN_FAILURE', '')

# if the user should be redirected to an error page on access token failure,
#   then define that redirect here, otherwise a 404 will be raised
SOCIAL_USER_REDIRECT_ON_ACCESS_TOKEN_FAILURE = getattr(settings,
    'SOCIAL_USER_REDIRECT_ON_ACCESS_TOKEN_FAILURE', '')

# this should be defined, if users should always be redirected to the
#   same page after authenticating. If either this value or the 'next' session
#   variable are not defined, then a 404 will be raised, because library
#   won't know where to redirect to.
SOCIAL_USER_REDIRECT_ON_AUTHENTICATION = getattr(settings,
    'SOCIAL_USER_REDIRECT_ON_AUTHENTICATION', '')