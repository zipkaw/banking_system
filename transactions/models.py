from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


User = settings.AUTH_USER_MODEL

class Credit(models.Model):
    user = models.ForeignKey(
        User,
        related_name='credits',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10.00'))
        ]
    )
    percent=models.DecimalField(
        decimal_places=2,
        max_digits=2,
        validators=[
            MinValueValidator(Decimal('1')),
            MaxValueValidator(Decimal('15'))
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    approval = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Diposit(models.Model):
    user = models.ForeignKey(
        User,
        related_name='deposits',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10.00'))
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    approval = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Withdrawal(models.Model):
    user = models.ForeignKey(
        User,
        related_name='withdrawals',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10.00'))
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    approval = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Interest(models.Model):
    user = models.ForeignKey(
        User,
        related_name='interests',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    approval = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
