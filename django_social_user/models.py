from django.contrib.auth.models import User
from django.db import models
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _


class SocialIdentity(models.Model):
    """
    A generic representation of an Identity on a social network.
    """
    # fields to make a unique id
    network = models.CharField(max_length=30,
        help_text='The name of the social network, should be defined on '
                  'extended GenericSocialUserBackend.')
    uid = models.CharField(max_length=255, help_text="The related network ID.")
    access_token = models.CharField(
        max_length=255, help_text="The access token for the social account.")
    access_token_expires = models.DateTimeField(null=True, blank=True)

    # fields to mirror user
    username = models.CharField(_('username'), max_length=255,
        help_text=_('Required. 255 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'))
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    email = models.EmailField(_('e-mail address'), blank=True)

    # link to a Django user when possible
    user = models.ForeignKey(User, null=True,
        help_text="The user associated with this Social Identity; nullable.")

    # data for the related social network
    _data = models.TextField(db_column='data', blank=True)
    def set_data(self, data):
        self._data = simplejson.dumps(data)
    def get_data(self):
        return simplejson.loads(self._data)
    data = property(get_data, set_data)

    class Meta:
        unique_together = (('network', 'uid'),)
