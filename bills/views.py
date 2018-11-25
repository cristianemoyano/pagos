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
    pay_total_debt,
    BILL_STATUSES,
)


def debt_list(request):
    code_list = [BILL_STATUSES.get('pending'), BILL_STATUSES.get('expired')]
    bill_statuses = get_bill_statuses(code_list)
    today = datetime.today()
    debts = Debt.objects.filter(status__in=bill_statuses).order_by('bill')
    total = debts.aggregate(Sum('total_owed')).get('total_owed__sum')
    if total:
        total = str(total)
    else:
        total = 0
    context = {
        'debts': debts,
        'total': total,
        'today': today
    }
    return render(
        request,
        'bills/debt_list.html',
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
