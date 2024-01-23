from django.db import models
from django.contrib.auth.models import User
import logging

applog = logging.getLogger('applog')
errorlog = logging.getLogger('errorlog')

class SuppliesGroup(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return str(self.name)


class SuppliesUsers(models.Model):
    ROLES_CHOICES = (
        ('teamlead', 'Руководитель группы'),
        ('employee', 'Сотрудник группы'),
        ('controller', 'Контролёр'),
        ('admin','Администратор')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLES_CHOICES)
    group = models.ForeignKey(SuppliesGroup, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user) + " - " + str(self.role)




class SupplyName(models.Model):
    TYPE_CHOICES = (
        ('cartridge', 'Картридж'),
        ('cable', 'Кабели, переходники'),
        ('mouse', 'Мышь'),
        ('keyboard', 'Клавиатура')
    )
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class SupplyRemain(models.Model):
    group = models.ForeignKey(SuppliesGroup, on_delete=models.CASCADE)
    supply = models.ForeignKey(SupplyName, on_delete=models.CASCADE)
    remains = models.IntegerField()

    def __str__(self):
        return str(self.group) + " - " + str(self.supply) + " - " + str(self.remains)

class IssueSupply(models.Model):
    timestamp_created = models.DateTimeField(auto_now_add=True, blank=True, null=True, editable=False)
    timestamp_modified = models.DateTimeField(auto_now=True, blank=True, null=True, editable=False)
    group = models.ForeignKey(SuppliesGroup, on_delete=models.CASCADE, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    supply = models.ForeignKey(SupplyRemain, on_delete=models.CASCADE, editable=False)
    # Вносимые пользователем параметры заявки на выдачу
    itsm_id = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    placement = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    device_model = models.CharField(max_length=100)

    def __str__(self):
        return  str(self.itsm_id) + " - " +  str(self.barcode) + " - " + str(self.supply.supply.name) + " - " + str(self.user)