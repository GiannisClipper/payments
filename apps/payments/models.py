from django.db import models

from django.contrib.auth import get_user_model

from funds.models import Fund
from genres.models import Genre


class Payment(models.Model):
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
        unique_together = (
            ('user', 'date', 'genre', 'incoming', 'outgoing', 'fund', 'remarks'),
            # Seems that unique_together does not work properly with null values
        )

        index_together = (
            ('user', 'date'),
        )

    def save(self, *args, **kwargs):

        # Remove leading or trailing spaces from strings
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(self, field.name)
                if value:
                    setattr(self, field.name, value.strip())

        # Field validations run here
        self.full_clean()

        super().save(*args, **kwargs)

    def update(self, **fields):
        '''Updates and returns a genre.'''

        for key, value in fields.items():
            setattr(self, key, value)

        self.save()

        return self

    def __str__(self):
        amount = self.incoming if self.genre.is_incoming else self.outgoing

        return f'{self.genre.name} {self.date} {amount} {self.remarks}'
