# -*- coding: utf-8 -*-

from zip.models import ZipRecord, FreeZipRecord, StationeryRecord, ZipIdea
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


class FreeZipRecordForm(ModelForm):
    class Meta:
        model = FreeZipRecord
        fields = '__all__'
        labels = {
            "zip": "Наименование",
            "amount": "Количество",
            "order": "Заказ",
            "comment": "Комментарий",
        }


class StationeryRecordForm(ModelForm):
    class Meta:
        model = StationeryRecord
        fields = '__all__'
        labels = {
            "zip": "Канцтовар",
            "amount": "Количество",
            "order": "Заказ",
            "comment": "Комментарий",
        }

class ZipIdeaForm(ModelForm):
    class Meta:
        model = ZipIdea
        fields = '__all__'
        labels = {
            "author":"От:",
            "topic":"Тема:",
            "body":"Идея:",
        }

