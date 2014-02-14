from django.conf.urls import patterns, include, url
from purchase import urls as purchase_urls
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myfinance.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^purchase/', include(purchase_urls)),
)
