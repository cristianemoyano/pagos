from django.conf import settings
from django.db import models
from django.utils import timezone


class BillType(models.Model):
    title = models.CharField(max_length=200)
    detail = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)

    def add(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class BillStatus(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=100)
    detail = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)

    def add(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Bill(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bill_type = models.ForeignKey(BillType, on_delete=models.CASCADE)
    frequency = models.IntegerField()
    title = models.CharField(max_length=200)
    currency_code = models.CharField(max_length=10)
    currency_symbol = models.CharField(max_length=10)
    reference = models.CharField(max_length=200)
    detail = models.TextField()
    expiration_day = models.IntegerField()
    charge = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_installments = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_count = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)

    def add(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Debt(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(default=timezone.now)
    total_owed = models.DecimalField(max_digits=10, decimal_places=2)
    total_month = models.DecimalField(max_digits=10, decimal_places=2)
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.ForeignKey(BillStatus, on_delete=models.CASCADE)
    installment_number = models.IntegerField()
    detail = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)

    def add(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return self.bill.title

class Payment(models.Model):
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE)
    detail = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(blank=True, null=True)

    def add(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return self.debt.bill.title
