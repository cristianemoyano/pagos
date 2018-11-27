from .models import (
    Debt,
    BillStatus,
    Payment,
)
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
import pytz

BILL_STATUSES = {
    'pending': 'PENDING',
    'paid': 'PAID',
    'expired': 'EXPIRED'
}


def find_debts_created(bill, expiration_date):
    return Debt.objects.filter(
        bill=bill,
        expiration_date=expiration_date
    )

def find_payments_created(debt):
    return Payment.objects.filter(debt=debt)


def create_debt(
    bill,
    expiration_date,
    status,
    installment_number=None,
):
        if not installment_number:
            installment_number = 0
        Debt.objects.create(
            bill=bill,
            total_owed=bill.amount,
            total_month=bill.amount,
            charge=bill.charge,
            installment_number=installment_number,
            detail=bill.detail,
            status=status,
            expiration_date=expiration_date
        )


def get_amount_of_debts(bill):
    d1 = bill.start_count
    d2 = timezone.now()
    diff = abs((d2 - d1).days)
    debts_count = round(diff / bill.frequency) + 1
    return debts_count


def get_expiration_date(bill):
    d1 = bill.start_count
    expiration_date = datetime(d1.year, d1.month, bill.expiration_day, tzinfo=pytz.UTC)
    return expiration_date


def get_bill_status(code):
    return BillStatus.objects.get(code=code)


def get_bill_statuses(code_list):
    return BillStatus.objects.filter(code__in=code_list)

def is_expired(expiration_date):
    today = timezone.now()
    today = datetime(today.year, today.month, today.day, tzinfo=pytz.UTC)
    if today > expiration_date:
        return True
    else:
        return False

def generate_pending_debts(bill):
    try:
        pending_status = get_bill_status(BILL_STATUSES.get('pending'))
        expired_status = get_bill_status(BILL_STATUSES.get('expired'))
        debts_count = get_amount_of_debts(bill)
        expiration_date = get_expiration_date(bill)
        if bill.frequency and not bill.total_installments:
            for i in range(0, debts_count):
                debts_created = find_debts_created(bill, expiration_date)
                if not debts_created:
                    if is_expired(expiration_date):
                        status = expired_status
                    else:
                        status = pending_status
                    create_debt(bill, expiration_date, status)
                expiration_date += timedelta(days=bill.frequency)
            return True
        elif bill.total_installments and bill.frequency:
            for i in range(0, debts_count):
                debts_created = find_debts_created(bill, expiration_date)
                if not debts_created:
                    installment_number = i + 1
                    if is_expired(expiration_date):
                        status = expired_status
                    else:
                        status = pending_status
                    create_debt(bill, expiration_date, status, installment_number)
                expiration_date += timedelta(days=bill.frequency)
            return True
        return False
    except Exception:
        return False

def pay_total_debt(id, detail):
    try:
        debt = Debt.objects.get(id=id)
        payments = find_payments_created(debt)
        if not payments:
            paid_status = get_bill_status(BILL_STATUSES.get('paid'))
            debt.status = paid_status
            debt.save()
            payment = Payment.objects.create(
                debt=debt,
                detail=detail,
            )
            return True
        else: 
            return False
    except Exception:
        return False