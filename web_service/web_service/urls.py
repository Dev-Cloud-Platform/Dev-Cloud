from django.conf.urls import patterns, include, url
from django.contrib import admin

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web_service.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
