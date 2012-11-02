from django.conf.urls import patterns, url

urlpatterns = patterns('django_social_user.views',
    url(r'^authenticate/(?P<network>\w+)/$', 'authenticate', name='authenticate'),
    url(r'^callback/(?P<network>\w+)/$', 'callback', name='callback'),
)
