import hmac
import requests

from hashlib import sha256

from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.encoding import force_bytes
from django.utils.decorators import method_decorator
from django.conf import settings

from .utils import VKApi, Groups
from .models import Community


class InIframeMixin(object):
    """..."""

    def dispatch(self, request, *args, **kwargs):
        """..."""
        try:
            gkeys = ('api_url', 'api_id', 'api_settings', 'viewer_id',
                'viewer_type', 'sid', 'secret', 'access_token', 'user_id',
                'group_id', 'is_app_user', 'auth_key', 'language',
                'parent_language', 'is_secure', 'stats_hash', 'ads_app_id', 
                'referrer', 'lc_name'
            )
            viewer_id = int(request.GET.get('viewer_id',0))
            viewer_type = int(request.GET.get('viewer_type',0))
            group_id = int(request.GET.get('group_id',0))
            sign = request.GET.get('sign')
            if sign and not group_id:
                self.request.session['viewer_id'] = None
                self.request.session['group_id'] = None

            params = ''
            for k in gkeys:
                params = params + request.GET[k]
            local_sign = hmac.new(
                settings.VK_APP_SECRET_KEY.encode('utf-8'),
                params.encode('utf-8'),
                sha256
            ).hexdigest()
            is_admin = False
            
                
            if sign and (local_sign == sign):
                if (viewer_type==4) and group_id>0:
                    is_admin = True
                    self.request.session['viewer_id'] = viewer_id
                    self.request.session['group_id'] = group_id
                else:
                    self.request.session['viewer_id'] = None
                    self.request.session['group_id'] = None

        except Exception as e:
            pass

        if not self.request.session.get('group_id'):
            raise Http404

        return super().dispatch(request, *args, **kwargs)


class IsInstalledMixin(object):
    """..."""

    def dispatch(self, request, *args, **kwargs):
        """..."""
        group_id = self.request.session.get('group_id')
        c, created = Community.objects.get_or_create(
            community_id=group_id
        )
        if not c.name:
            c.save()

        try:
            token = c.tokens.first().token
        except Exception as e:
            token = False

        api = VKApi(
            token,
            proxies=settings.REQUESTS_PROXY_DICT
        )
        this_listen_url = self.request.build_absolute_uri(
            reverse('bot:listen')
        )
        this_listen_url = this_listen_url.replace('http://', 'https://')
        try:
            vk_response = api.groups.get_callback_servers(group_id)
            servers = vk_response.get('response').get('items')
            remote = list(filter(
                lambda x: x['url']==this_listen_url,
                servers
            ))[0]
        except:
            remote = dict()
        if remote.get('status')!='ok' and not settings.SKIP_INSTALLED_MIXIN:
            return redirect(reverse('community:token:create'))

        return super().dispatch(request, *args, **kwargs)
