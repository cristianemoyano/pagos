from django.urls import (
    path,
)
from . import views


urlpatterns = [
    path('', views.debt_list, name='home'),
    path('generate/', views.generate_pending_debts_view, name='generate_pending_debts'),
    path('pay/<int:id>/', views.pay_debt, name='pay_debt'),
]
