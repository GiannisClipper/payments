from django.db import models
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from core.models import CustomBaseModel
from funds.models import Fund

from .constants import (
    USER_REQUIRED,
    CODE_REQUIRED,
    NAME_REQUIRED,
    CODE_EXISTS,
    NAME_EXISTS,
    FUND_INVALID,
)

class Genre(CustomBaseModel):
    '''Model represents and stores genres.'''

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        error_messages={
            'required': USER_REQUIRED,
            'null': USER_REQUIRED,
            'blank': USER_REQUIRED,
        }
    )

    code = models.CharField(
        max_length=8,
        null=False,
        blank=False,
        error_messages={
            'required': CODE_REQUIRED,
            'null': CODE_REQUIRED,
            'blank': CODE_REQUIRED,
        }
    )

    name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        error_messages={
            'required': NAME_REQUIRED,
            'null': NAME_REQUIRED,
            'blank': NAME_REQUIRED,
        }
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
        # constraints = (
        #     models.UniqueConstraint(
        #         fields=('user', 'code'),
        #         name='unique_code'
        #     ),
        #     models.UniqueConstraint(
        #         fields=('user', 'name'),
        #         name='unique_name'
        #     ),
        # )

        unique_together = (
            ('user', 'code'),
            ('user', 'name'),
        )

        index_together = (
            ('user', 'code'),
            ('user', 'name'),
        )

    def unique_error_message(self, model_class, unique_check):

        if model_class == type(self) and unique_check == ('user', 'code'):
            return CODE_EXISTS

        elif model_class == type(self) and unique_check == ('user', 'name'):
            return NAME_EXISTS

        else:
            return super().unique_error_message(model_class, unique_check)

    def full_clean(self):

        super().full_clean()

        # Check `user` integrity as the same owner of `genre` and `fund`

        if self.fund and self.fund.user.pk != self.user.pk:
            raise IntegrityError({'fund': FUND_INVALID})

    def __str__(self):
        return f'{self.name}'
