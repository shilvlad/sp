# -*- coding: utf-8 -*-

from .models import IssueSupply
from django.forms import ModelForm


class IssueSupplyForm(ModelForm):
    class Meta:
        model = IssueSupply
        fields = '__all__'
        labels = {
            "itsm_id" : "Номер задачи",
            "recipient" : "Пользователь",
            "placement" : "Местоположение",
            "barcode" : "Баркод",
        }


