# -*- coding: utf-8 -*-

from django.shortcuts import render


def purchase_importer_form(request):
    import_message = ''
    if request.method == 'POST':
        import_message = import_data(request)
    return render(
        request,
        'purchase_importer_form.html',
        {'message': import_message}
    )


def import_data(request):
    return 'Importacao efetuada com sucesso'
