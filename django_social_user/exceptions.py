class MissingRequiredSetting(ValueError):
    """
    Throw when a required setting value is not available.
    """
    def __init__(self, setting_name, *args, **kwargs):
        l = list(args)
        l.insert(0, "Please defined '%s' in your settings.py" % setting_name)
        super(self, MissingRequiredSetting).__init__(*args, **kwargs)


class SocialOauthDictFailed(ValueError):
    """
    Throw when backend is unable to fetch or parse data for get_oauth_dict.
    """
    pass


class SocialIdentityOwnedByAnotherUser(ValueError):
    """
    Thrown when the generic backend detects that the social identity
    is already owned by another user.
    """
    pass

class DoNotAuthenticate(ValueError):
    """
    Thrown when the django project wishes to skip the authentication
    backend.
    """
    pass
