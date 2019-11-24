from django.db import models
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from core.models import CustomBaseModel
from funds.models import Fund
from genres.models import Genre


class Payment(CustomBaseModel):
    '''Model represents and stores payments.'''

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=False,
    )

    date = models.DateField(
        db_index=True,
        null=False,
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        null=False,
    )

    incoming = models.FloatField(
        null=True,
        default=0,
    )

    outgoing = models.FloatField(
        null=True,
        default=0,
    )

    fund = models.ForeignKey(
        Fund,
        on_delete=models.CASCADE,
        null=False,
    )

    remarks = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        default='',
    )

    class Meta:
        unique_together = (
            # Unique constraint does not work properly with null values so we need
            # to convert incoming/outgoing None to 0 as well as remarks None to ''
            ('user', 'date', 'genre', 'incoming', 'outgoing', 'fund', 'remarks'),
        )

        index_together = (
            ('user', 'date'),
        )

    def full_clean(self):
        # An `incoming` value is necessary for unique_together validation
        if getattr(self, 'incoming') is None:
            setattr(self, 'incoming', 0)

        # An `outgoing` value is necessary for unique_together validation
        if getattr(self, 'outgoing') is None:
            setattr(self, 'outgoing', 0)

        # A `remarks` value is necessary for unique_together validation
        if getattr(self, 'remarks') is None:
            setattr(self, 'remarks', '')

        super().full_clean()

        # Check `user` integrity as the same owner of `payment`, `genre` and `fund`
        errors = {}

        if self.genre and self.genre.user.pk != self.user.pk:
            errors['genre'] = 'Genre.user integrity error.'

        if self.fund and self.fund.user.pk != self.user.pk:
            errors['fund'] = 'Fund.user integrity error.'

        if errors:
            raise IntegrityError(errors)


    def __str__(self):
        amount = self.incoming if self.genre.is_incoming else self.outgoing

        return f'{self.genre.name} {self.date} {amount} {self.remarks}'
