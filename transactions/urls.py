from django.urls import path

from .views import deposit_view, withdrawal_view, approval_credit_view, approval_deposit_view,  approval_withdrawal_view


app_name = 'transactions'

urlpatterns = [
    # url(r'^$', home_view, name='home'),
    path('deposit/', deposit_view, name='deposit'),
    path('withdrawal/', withdrawal_view, name='withdrawal'),
    path('approve_credit/', approval_credit_view, name='approval_credit'),
    path('approve_deposit/', approval_deposit_view, name='approval_deposit'),
    path('approve_withdrawal/', approval_withdrawal_view, name='approval_withdrawal'),
]
