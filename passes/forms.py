# -*- coding: utf-8 -*-
from passes.models import Passes
from django.forms import ModelForm
from django import forms


#class DateInput(forms.DateInput()):
#    input_type = 'date'


class PassesForm(ModelForm):
    #passexpired = forms.DateField(widget=DateInput)
    #passexpired = forms.DateField()

    class Meta:
        model = Passes
        fields = ['owner','passexpired', 'passnumber','passtype']
        labels = {
            "owner": "ФИО",
            "passexpired": "Пропуск истекает",
            "passnumber": "Номер пропуска",
            "passtype": "Тип пропуска",

        }
        widgets = {
            'passexpired': forms.DateInput(
                format=('%Y-%m-%d'),  # Формат, в котором ХРАНИТСЯ дата
                attrs = {
                    'class':'form-control',
                    'type':'date'
                }
            ),
        }
