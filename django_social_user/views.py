from logging import getLogger

from django.contrib.auth import authenticate as auth, login, get_backends
from django.http import Http404
from django.shortcuts import redirect

from django_social_user import options
from django_social_user.exceptions import (DoNotAuthenticate,
    SocialOauthDictFailed, MissingRequiredSetting)
from django_social_user.signals import (django_social_user_pre_callback,
    django_social_user_pre_auth, django_social_user_post_callback)

logger = getLogger('django_social_user:views')

SK_AUTH_REDIRECT = 'django_social_user:authentication_redirect'
SK_REQUEST_TOKEN = 'django_social_user:oauth_request_token'


def get_network_backend_or_404(network):
    """
    Fetch the network backend from django's list of backends or throw
    a 404 exception.
    """
    if network:
        for backend in get_backends():
            if network == getattr(backend, 'network', None):
                return backend

    logger.exception(
        'Attempting to authenticate unregistered backend %s' % network)
    raise Http404


def authenticate(request, network):
    """
    Invoked before redirecting the user to a social network. This view
    sets up necessary information for that needed in the callback for
    the oauth exchange.
    """
    backend = get_network_backend_or_404(network)
    django_social_user_pre_auth.send(None, request=request)

    try:
        oauth_request_token = backend.get_oauth_request_token()
        request.session[SK_REQUEST_TOKEN] = oauth_request_token
        url_prefix = 'https' if request.is_secure() else 'http'
        url_prefix += '://%s' % request.META['HTTP_HOST']
        return redirect(backend.get_oauth_authorization_url(
            oauth_request_token,
            url_prefix=url_prefix,
            params=request.GET.dict()))
    except:
        logger.exception('Authentication failed for %s' % network)
        return redirect_or_error(
            options.REDIRECT_ON_REQUEST_TOKEN_FAILURE,
            options.KEY_REQUEST_TOKEN_FAILURE)


def callback(request, network):
    """
    This is the authentication view called by social network after the
    user authenticates via the social network.
    """
    oauth_request_token = request.session.get(SK_REQUEST_TOKEN)

    if not oauth_request_token:
        raise Http404

    backend = get_network_backend_or_404(network)

    try:
        access_token, access_token_expires = backend.get_oauth_access_token(
            request, oauth_request_token)
    except:
        logger.exception('Callback failed for %s' % network)
        return redirect_or_error(
            options.REDIRECT_ON_ACCESS_TOKEN_FAILURE,
            options.KEY_ACCESS_TOKEN_FAILURE)

    responses = django_social_user_pre_callback.send_robust(
                                    None,
                                    request=request,
                                    network=network,
                                    access_token=access_token,
                                    access_token_expires=access_token_expires)

    # Check to see if the pre_callback signal raised an exception to skip
    # the authentication backend.
    if not any([isinstance(response, DoNotAuthenticate)
                for receiver, response in responses]):
        # If the user is already authenticated, pass into the backend
        # so that the social identity can be associated to the user.
        user = request.user if request.user.is_authenticated() else None

        user = auth(
            network=network, access_token=access_token,
            access_token_expires=access_token_expires, user=user)

        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                # todo: handle this better
                raise SocialOauthDictFailed('User is not active')
        else:
            raise SocialOauthDictFailed('User not returned from authorization')

    django_social_user_post_callback.send(None, request=request)

    # redirect to the session value or the default redirect value
    return redirect_or_error(
        options.REDIRECT_ON_AUTHENTICATION, options.KEY_AUTHENTICATION,
        override=request.session.get(SK_AUTH_REDIRECT))


def redirect_or_error(opt, key, override=''):
    """
    Tests if a redirect URL is available and redirects, or raises a
    MissingRequiredSetting exception.
    """
    r = (override or opt)

    if r:
        return redirect(r)
    raise MissingRequiredSetting('%s.%s' % (
        options.KEY_DATA_DICT, key))
