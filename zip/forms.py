# -*- coding: utf-8 -*-

from zip.models import ZipRecord
from django.forms import ModelForm

class ZipRecordForm(ModelForm):
    class Meta:
        model = ZipRecord
        fields = '__all__'
        labels = {
            "zip": "Наименование",
            "amount": "Количество",
            "order": "Заказ",
            "comment": "Комментарий",
        }