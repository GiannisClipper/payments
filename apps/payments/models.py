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
        blank=False,
    )

    date = models.DateField(
        db_index=True,
        null=False,
        blank=False,
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    incoming = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True,
    )

    outgoing = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True,
    )

    fund = models.ForeignKey(
        Fund,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    remarks = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                # Unique constraint does not work properly with null values so we convert 
                # incoming/outgoing None's to zeroes as well as remarks None to blank
                fields=('user', 'date', 'genre', 'incoming', 'outgoing', 'fund', 'remarks'),
                name='unique_payment'
            ),
        )

        index_together = (
            ('user', 'date'),
        )

    def clean(self):
        # Unique constraint does not work properly with null values so we convert 
        # incoming/outgoing None's to zeroes as well as remarks None to blank
        value = getattr(self, 'incoming')
        if value == None:
            setattr(self, 'incoming', 0)

        value = getattr(self, 'outgoing')
        if value == None:
            setattr(self, 'outgoing', 0)

        value = getattr(self, 'remarks')
        if value == None:
            setattr(self, 'remarks', '')

        super().clean()

    def __str__(self):
        amount = self.incoming if self.genre.is_incoming else self.outgoing

        return f'{self.genre.name} {self.date} {amount} {self.remarks}'
