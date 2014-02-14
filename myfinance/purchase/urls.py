from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^pdi/', 'purchase.views.import_purchase_data', name='import_purchase_data'),
)
