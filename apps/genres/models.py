from django.db import models
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from core.models import CustomBaseModel
from funds.models import Fund


class Genre(CustomBaseModel):
    '''Model represents and stores genres.'''

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    code = models.CharField(
        max_length=8,
        null=False,
        blank=False,
    )

    name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
    )

    is_incoming = models.BooleanField(
        default=False
    )

    fund = models.ForeignKey(
        Fund,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = (
            ('user', 'code'),
            ('user', 'name'),
        )

        index_together = (
            ('user', 'code'),
            ('user', 'name'),
        )

    def full_clean(self):
        super().full_clean()

        # Check `user` integrity as the same owner of `genre` and `fund`
        if self.fund and self.fund.user.pk != self.user.pk:
            raise IntegrityError({'fund': 'Fund.user integrity error.'})

    def __str__(self):
        return f'{self.name}'
