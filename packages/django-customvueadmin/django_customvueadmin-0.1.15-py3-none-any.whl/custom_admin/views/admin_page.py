import json

from django.conf import os, settings
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.views import View

TEMPLATE_NOT_FOUND = '''
Custom admin cannot find template "{template}".
Make sure settings.TEMPLATES contains 'APP_DIRS': True
'''


class CustomAdminView(View):
    '''
    # Settings in case of h2ttps:
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    '''

    template = 'custom_admin/admin_index.html'

    def get(self, request):
        static_prefix = settings.CUSTOM_ADMIN.get('static_prefix') or '/static/custom_admin'

        admin_settings = {
            'title': settings.CUSTOM_ADMIN.get('title'),
            'base_admin_url': settings.CUSTOM_ADMIN.get('base_admin_url') or 'admin/',
            'static_prefix': static_prefix,
            'favicon_path': settings.CUSTOM_ADMIN.get('favicon_path') or os.path.join(static_prefix, 'favicon.ico'),
            'logo_image_path': settings.CUSTOM_ADMIN.get('logo_image_path') or os.path.join(static_prefix, 'default-logo.png'),
            'auth_header_prefix': settings.CUSTOM_ADMIN.get('auth_header_prefix') or 'Token',
        }

        if not admin_settings.get('backend_prefix'):
            admin_settings['backend_prefix'] = request.build_absolute_uri('/custom_admin/')

        context = {
            'SETTINGS': admin_settings,
            'SETTINGS_JSON': json.dumps(admin_settings),
        }

        try:
            return render(request, self.template, context)
        except TemplateDoesNotExist as e:
            raise TemplateDoesNotExist(TEMPLATE_NOT_FOUND.format(template=self.template)) from e
