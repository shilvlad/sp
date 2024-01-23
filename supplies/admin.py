from django.contrib import admin
from .models import SuppliesUsers, SuppliesGroup, SupplyName, SupplyRemain, IssueSupply

# Register your models here.
admin.site.register(SuppliesUsers)
admin.site.register(SuppliesGroup)
admin.site.register(SupplyName)
admin.site.register(SupplyRemain)

class IssueSupplyAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp_created','timestamp_modified', 'group', 'user', 'supply')
admin.site.register(IssueSupply, IssueSupplyAdmin)