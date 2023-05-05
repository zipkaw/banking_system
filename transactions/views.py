from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import User
from .models import Credit, Diposit, Withdrawal
from .forms import (
    DepositForm,
    WithdrawalForm,
    CreditForm,
    CreditApprovalForm,
    DipositApprovalForm,
    WithdrawalApprovalForm,
)

CreditApprovalFormSet = modelformset_factory(model=Credit, form=CreditApprovalForm, fields=('approval','amount'))
DepositApprovalFormSet = modelformset_factory(model=Diposit, form=DipositApprovalForm, fields=('approval','amount'))
WithdrawalFormSet = modelformset_factory(model=Withdrawal, form=WithdrawalApprovalForm, fields=('approval','amount'))

@login_required()
@permission_required('is_staff')
def approval_credit_view(request):
    queryset=Credit.objects.filter(Q(approval=False))
    if len(queryset) == 0:
        messages.success(request, 'There are none approval application')
        return redirect("home")

    formset = CreditApprovalFormSet(request.POST or None, queryset=queryset)
    if formset.is_valid():
        for form in formset:
            credit = form.save(commit=False)
            if credit.approval == True:
                #send document to user email

                credit.save()
                credit.user.account.balance += credit.amount
                credit.user.account.save()

    context = {
        "title": "Credits to approve",
        "formset": formset,
    }
    return render(request, "transactions/formset.html", context)

@login_required()
@permission_required('is_staff')
def approval_deposit_view(request):
    queryset=Diposit.objects.filter(Q(approval=False))
    if len(queryset) == 0:
        messages.success(request, 'There are none approval application')
        return redirect("home")

    formset = DepositApprovalFormSet(request.POST or None, queryset=queryset)

    if formset.is_valid():
        for form in formset:
            deposit = form.save(commit=False)
            if deposit.approval == True:
                #send document to user email
                deposit.save()
                try: 
                    deposit.user.account.balance += deposit.amount
                    deposit.user.account.save()
                except ObjectDoesNotExist:
                    pass
                return redirect("transactions:approval_deposit")
         
    context = {
        "title": "Deposits to approve",
        "formset": formset,
    }
    return render(request, "transactions/formset.html", context)


@login_required()
@permission_required('is_staff')
def approval_withdrawal_view(request):
    queryset=Withdrawal.objects.filter(approval=False)
    if len(queryset) == 0:
        messages.success(request, 'There are none approval application')
        return redirect("home")

    formset = WithdrawalFormSet(request.POST or None, queryset=queryset)
    if formset.is_valid():
        for form in formset:
            withdrawal = form.save(commit=False)
            if withdrawal.approval == True:
                #send document to user email
                withdrawal.save()
                withdrawal.user.account.balance -= withdrawal.amount
                withdrawal.user.account.save()
    context = {
        "title": "Credits to approve",
        "formset": formset,
    }
    return render(request, "transactions/formset.html", context)


@login_required()
def deposit_view(request):
    form = DepositForm(request.POST or None)

    if form.is_valid():
        deposit = form.save(commit=False)
        deposit.user = request.user
        deposit.save()
        # adds users deposit to balance.
        messages.success(request, 'You Have Deposited {} $.'
                         .format(deposit.amount))
        return redirect("home")

    context = {
        "title": "Deposit",
        "form": form
    }
    return render(request, "transactions/form.html", context)


@login_required()
def credit_view(request):
    form = CreditForm(request.POST or None)

    if form.is_valid():
        credit = form.save(commit=False)
        credit.user = request.user
        credit.save()
        # adds users credit to balance.
        credit.user.account.balance += credit.amount
        credit.user.account.save()
        messages.success(request, 'You Have credited {} $.'
                         .format(credit.amount))
        return redirect("home")

    context = {
        "title": "Credit",
        "form": form
    }
    return render(request, "transactions/form.html", context)


@login_required()
def withdrawal_view(request):
    form = WithdrawalForm(request.POST or None, user=request.user)

    if form.is_valid():
        withdrawal = form.save(commit=False)
        withdrawal.user = request.user
        withdrawal.save()
        # subtracts users withdrawal from balance.
        withdrawal.user.account.balance -= withdrawal.amount
        withdrawal.user.account.save()

        messages.success(
            request, 'You Have Withdrawn {} $.'.format(withdrawal.amount)
        )
        return redirect("home")

    context = {
        "title": "Withdraw",
        "form": form
    }
    return render(request, "transactions/form.html", context)
