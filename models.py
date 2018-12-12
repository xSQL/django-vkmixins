from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .utils import VKApi, Groups as GroupsAPI


User = get_user_model()



class Community(models.Model):
    """..."""
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name')
    )
    community_id = models.PositiveIntegerField(
        verbose_name=_('Community id')
    )
    callback_key = models.CharField(
        max_length=16,
        default='',
        verbose_name = _('Callback secret key')
    )
    extensions = models.ManyToManyField(Extension)

    def save(self, *args, **kwargs):
        api = VKApi(
            token=settings.VK_UACCESS_TOKEN,
            proxies=settings.REQUESTS_PROXY_DICT
        )
        vk_request = api.groups.get_by_id(self.community_id)
        response = vk_request.get('response')
        self.name = response[0].get('name')
        super().save(*args, **kwargs)

    def __str__(self):
        """..."""
        return '{0} ({1})'.format(
            self.name,
            self.community_id
        )

