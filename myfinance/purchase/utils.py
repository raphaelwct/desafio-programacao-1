# -*- coding: utf-8 -*-
from purchase import models


def import_data(request):
    purchase_total = 0

    purchase_file = request.FILES['purchase_file']
    for line in read_file_lines(purchase_file):
        purchase_data = parse_purchase_file_data(line)
        save_purchase_data(purchase_data)
        purchase_total += calc_purchase_total(purchase_data)

    return {
        'import_feedback': "Importacao efetuada com sucesso.",
        'purchase_total': "A receita bruta total foi de R$ %s." % purchase_total
    }


def calc_purchase_total(parsed_line):
    item_price = float(parsed_line['item_price'])
    purchase_count = int(parsed_line['purchase_count'])
    return item_price * purchase_count


def read_file_lines(purchase_file):
    purchase_file = iter(purchase_file)
    purchase_file.next()
    for line in purchase_file:
        yield (tuple(line.split('\t')))


def parse_purchase_file_data(file_line):
    return {
        'purchaser_name': file_line[0],
        'item_description': file_line[1],
        'item_price': float(file_line[2]),
        'merchant_address': file_line[4],
        'merchant_name': file_line[5],
        'purchase_count': int(file_line[3])
    }


def save_purchase_data(parsed_data):
    purchaser = models.Purchaser.objects.get_or_create(name=parsed_data['purchaser_name'])[0]
    item = models.Item.objects.get_or_create(
        description=parsed_data['item_description'], price=float(parsed_data['item_price']))[0]
    merchant = models.Merchant.objects.get_or_create(
        address=parsed_data['merchant_address'], name=parsed_data['merchant_name'])[0]
    purchase = models.Purchase(
        purchaser=purchaser,
        item=item,
        merchant=merchant,
        count=parsed_data['purchase_count']
    )
    purchase.save()
