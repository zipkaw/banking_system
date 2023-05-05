from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.core.exceptions import ObjectDoesNotExist

from .models import Diposit, Withdrawal, Credit

class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ["amount"]

class DepositForm(forms.ModelForm):
    class Meta:
        model = Diposit
        fields = ["amount"]


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ["amount"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WithdrawalForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if self.user.account.balance < amount:
            raise forms.ValidationError(
                'You Can Not Withdraw More Than You Balance.'
            )
        return amount


class BaseApprovalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super(BaseApprovalForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False
        try:
            self.user = self.instance.user
            self.username = self.instance.user.email
        except ObjectDoesNotExist:
            self.username = ''
    
        self.fields['username'] = forms.CharField(disabled=True, initial=self.username)

    amount = forms.CharField(disabled=True)

    class Meta:
        fields = ["approval"]


class CreditApprovalForm(BaseApprovalForm):

    class Meta(BaseApprovalForm.Meta):
        model=Credit


class DipositApprovalForm(BaseApprovalForm):
    def __init__(self, *args, **kwargs) -> None:
        super(DipositApprovalForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False

    class Meta(BaseApprovalForm.Meta):
        model=Diposit

    
class WithdrawalApprovalForm(BaseApprovalForm):
    class Meta(BaseApprovalForm.Meta):
        model=Withdrawal
