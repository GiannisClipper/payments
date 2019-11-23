from django.db import models
from django.contrib.auth import get_user_model

from core.models import CustomBaseModel


class Fund(CustomBaseModel):
    '''Model represents and stores funds.'''

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

    class Meta:
        unique_together = (
            ('user', 'code'),
            ('user', 'name'),
        )

        index_together = (
            ('user', 'code'),
            ('user', 'name'),
        )

    def __str__(self):
        return f'{self.name}'
