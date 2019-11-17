from django.db import models


class CustomBaseModel(models.Model):
    '''A base model customization.'''

    class Meta:
        abstract=True

    # There are three steps involved in validating a model:
    # Validate the model fields - Model.clean_fields()
    # Validate the model as a whole - Model.clean()
    # Validate the field uniqueness - Model.validate_unique()
    # All three steps are performed when you call full_clean() method.

    def clean_fields(self, *args, **kwargs):
        # Remove leading or trailing spaces from strings
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(self, field.name)
                if value != None:
                    setattr(self, field.name, value.strip())

        super().clean_fields(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Validations are performed here
        self.full_clean()

        super().save(*args, **kwargs)

    def update(self, **fields):
        # Update and return an object

        for key, value in fields.items():
            setattr(self, key, value)

        self.save()

        return self
