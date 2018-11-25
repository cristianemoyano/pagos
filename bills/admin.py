from django.contrib import admin
from .models import (
    BillType,
    BillStatus,
    Bill,
    Debt,
    Payment,
)

admin.site.register(BillType)
admin.site.register(BillStatus)
admin.site.register(Bill)
admin.site.register(Debt)
admin.site.register(Payment)