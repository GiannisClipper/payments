from django.db import models
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
    )

    outgoing = models.FloatField(
        null=True,
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
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                # Unique constraint does not work properly with null values so we need
                # to convert incoming/outgoing None to 0 as well as remarks None to ''
                fields=('user', 'date', 'genre', 'incoming', 'outgoing', 'fund', 'remarks'),
                name='unique_payment'
            ),
        )

        index_together = (
            ('user', 'date'),
        )

    def full_clean(self):
        # Unique constraint does not work properly with null values so we need
        # to convert incoming/outgoing None to 0 as well as remarks None to ''
        value = getattr(self, 'incoming')
        if value == None:
            setattr(self, 'incoming', 0)

        value = getattr(self, 'outgoing')
        if value == None:
            setattr(self, 'outgoing', 0)

        value = getattr(self, 'remarks')
        if value == None:
            setattr(self, 'remarks', '')

        super().full_clean()

    def __str__(self):
        amount = self.incoming if self.genre.is_incoming else self.outgoing

        return f'{self.genre.name} {self.date} {amount} {self.remarks}'
