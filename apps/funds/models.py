from django.db import models

from django.contrib.auth import get_user_model


class Fund(models.Model):
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
        '''Updates and returns a fund.'''

        for key, value in fields.items():
            setattr(self, key, value)

        self.save()

        return self

    def __str__(self):
        return f'{self.name}'
