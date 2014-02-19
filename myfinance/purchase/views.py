# -*- coding: utf-8 -*-

from django.shortcuts import render
from purchase import utils


def purchase_importer_form(request):
    import_message = ''
    if request.method == 'POST':
        import_message = utils.import_data(request)
    return render(
        request,
        'purchase_importer_form.html',
        import_message
    )
