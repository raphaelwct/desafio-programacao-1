from django.conf.urls import patterns, include, url
from purchase import urls as purchase_urls

urlpatterns = patterns('',
    url(r'^purchase/', include(purchase_urls)),
)
