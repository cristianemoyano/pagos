from django import forms
from .models import (
    Debt,
    Bill,
    Payment,
)

class GenerateDebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = [
            'bill',
        ]
    bill_model = Bill.objects.all()
    bill = forms.ModelChoiceField(
        queryset=bill_model,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
    )

class PayDebtForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'detail'
        ]
