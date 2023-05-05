from django.db.models import Sum, Q
from django.shortcuts import render

from transactions.models import Diposit, Withdrawal, Interest, Credit


def home(request):
    if not request.user.is_authenticated:
        return render(request, "core/index.html", {})
    else:
        user = request.user
        deposit = Diposit.objects.filter(Q(user=user) & Q(approval = True))
        deposit_sum = deposit.aggregate(Sum('amount'))['amount__sum']
        credit = Credit.objects.filter(Q(user=user) & Q(approval = True))
        credit_sum = credit.aggregate(Sum('amount'))['amount__sum']
        withdrawal = Withdrawal.objects.filter(Q(user=user) & Q(approval = True))
        withdrawal_sum = withdrawal.aggregate(Sum('amount'))['amount__sum']
        interest = Interest.objects.filter(Q(user=user) & Q(approval = True))
        interest_sum = interest.aggregate(Sum('amount'))['amount__sum']

        context = {
                    "user": user,
                    "deposit": deposit,
                    "deposit_sum": deposit_sum,
                    "credit": credit,
                    "credit_sum": credit_sum,
                    "withdrawal": withdrawal,
                    "withdrawal_sum": withdrawal_sum,
                    "interest": interest,
                    "interest_sum": interest_sum,
                  }

        return render(request, "core/transactions.html", context)


def about(request):
    return render(request, "core/about.html", {})
