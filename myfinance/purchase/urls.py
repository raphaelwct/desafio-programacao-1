from django.conf.urls import patterns, url

urlpatterns = patterns('', url(r'^pdi/', 'purchase.views.purchase_importer_form'),)
