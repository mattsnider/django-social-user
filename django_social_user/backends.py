from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.models import User
from django.utils import simplejson, timezone

from django_social_user.exceptions import SocialIdentityOwnedByAnotherUser
from django_social_user.models import SocialIdentity


class GenericSocialUserBackend(RemoteUserBackend):
    """
    Abstract backend class to be overwritten with network specific logic.
    """
    network = None

    def authenticate(self, network=None, access_token=None,
        access_token_expires=None, user=None):
        """
        Attempts to fetch and process remove social account data in order to
        authenticate in a generic way.
        """
        # authentication is not for this backend
        if not (self.network == network and access_token):
            raise TypeError

        # use oauth token to fetch the oauth object
        oauth_obj, uid = self.get_oauth_dict(access_token)

        email = self.get_email(oauth_obj)
        first_name = self.get_first_name(oauth_obj)
        last_name = self.get_last_name(oauth_obj)
        username = self.get_username(oauth_obj)

        social_identity, created = SocialIdentity.objects.get_or_create(
            network=network, uid=uid, defaults={
                'data': simplejson.dumps(oauth_obj),
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
            })

        # this social identity already exists
        if not created:
            # a user was passed in, make sure that it matches the user on
            #   the social identity
            if (user and social_identity.user_id and
                user.id != social_identity.user_id):
                raise SocialIdentityOwnedByAnotherUser

        # update the social identity with the provided user
        if not social_identity.user_id and user:
            social_identity.user = user
            social_identity.save()

        # check the access tokens
        if not hasattr(social_identity, 'access_token_expires'):
            # The account doesn't have an expiration property for its
            # access tokens. Simply compare the tokens and save.
            if social_identity.access_token != access_token:
                social_identity.access_token = access_token
                social_identity.save()
        else:
            # if your database value for access_token_expires has timezone
            # data, then we need to localize the access_token_expires provided
            # by facebook to that timezone for comparison (I assume that
            # your database and Django app use the same timezone)
            if social_identity.access_token_expires.tzinfo:
                if access_token_expires and timezone.get_default_timezone():
                    access_token_expires = timezone.make_aware(
                        access_token_expires, timezone.get_default_timezone())

            # Only update the access token if there isn't currently
            # one or if the new one expires later than the current one
            # (or if the current one doesn't have an expiration date).
            new_token_expires_later = (
                social_identity.access_token_expires and
                access_token_expires and
                access_token_expires > social_identity.access_token_expires)
            if (not social_identity.access_token or
                not social_identity.access_token_expires or
                new_token_expires_later):
                social_identity.access_token = access_token
                social_identity.access_token_expires = access_token_expires
                social_identity.save()

        if not user:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()

        # update the user on the social_identity
        if user and not social_identity.user_id:
            social_identity.user = user
            social_identity.save()

        return user

    def get_email(self, oauth_obj):
        """
        Get the email from the oauth object
        """
        raise NotImplementedError()

    def get_first_name(self, oauth_obj):
        """
        Get the first name from the oauth object
        """
        raise NotImplementedError()

    def get_last_name(self, oauth_obj):
        """
        Get the last name from the oauth object
        """
        raise NotImplementedError()

    def get_oauth_access_token(self, request, oauth_request_token):
        """
        Get the access token using the oauth request token and the data
        provided on the request. Should raise the appropriate exception
        if the data is invalid.
        """
        pass

    def get_oauth_authorization_url(self, oauth_request_token, url_prefix=''):
        """
        Create the authorization URL for redirect to social network.
        """
        raise NotImplementedError()

    def get_oauth_dict(self, access_token):
        """
        Uses the access token to find the oauth object,
        then returns it and the account uid:
        return (oauth_object, uid,)
        Raise SocialOauthDictFailed when response is invalid
        """
        raise NotImplementedError()

    def get_oauth_request_token(self):
        """
        Get the oauth request token from the network API.
        """
        raise NotImplementedError()

    def get_username(self, oauth_obj):
        """
        Get the username from the oauth object
        """
        raise NotImplementedError()
