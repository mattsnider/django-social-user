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