from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Sum
from .models import Debt
from .forms import (
    GenerateDebtForm,
    PayDebtForm,
)
from .domains import (
    generate_pending_debts,
    get_bill_statuses,
    get_bill_status,
    pay_total_debt,
    BILL_STATUSES,
)
from dateutil.relativedelta import relativedelta

def debt_list(request):
    
    today = datetime.today()
    next_month = today + relativedelta(months=+1)

    code_list = [BILL_STATUSES.get('pending'), BILL_STATUSES.get('expired')]
    bill_statuses = get_bill_statuses(code_list)
    debts_this_month = Debt.objects.filter(
        status__in=bill_statuses,
        expiration_date__month=today.month
    ).order_by('bill')
    total_this_month = debts_this_month.aggregate(Sum('total_owed')).get('total_owed__sum')
    
    debts_next_month = Debt.objects.filter(
        status__in=bill_statuses,
        expiration_date__month=today.month+1
    ).order_by('bill')
    total_next_month = debts_next_month.aggregate(Sum('total_owed')).get('total_owed__sum')
    
    paid_status = get_bill_status(BILL_STATUSES.get('paid'))
    paids = Debt.objects.filter(status=paid_status).order_by('bill')

    if total_this_month:
        total_this_month = str(total_this_month)
    else:
        total_this_month = 0
    
    if total_next_month:
        total_next_month = str(total_next_month)
    else:
        total_next_month = 0

    context = {
        'debts': debts_this_month,
        'next_debts': debts_next_month,
        'total': total_this_month,
        'next_total': total_next_month,
        'today': today,
        'next_month': next_month,
        'paids': paids,
    }
    return render(
        request,
        'bills/home.html',
        context=context
    )


def generate_pending_debts_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GenerateDebtForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            bill = form.cleaned_data['bill']
            debts_generated = generate_pending_debts(bill)
            if debts_generated:
                return HttpResponseRedirect('/')
            else:
                form = GenerateDebtForm()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GenerateDebtForm()
    return render(
        request,
        'bills/generate_pending_debts.html',
        {'form': form}
    )

def pay_debt(request, id):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PayDebtForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            detail = form.cleaned_data['detail']
            response = pay_total_debt(id, detail)
            if response:
                return HttpResponseRedirect('/')
    else:
        form = PayDebtForm()
    return render(
        request,
        'bills/pay.html',
        context={
            'form': form,
            'id': id
        }
    )
