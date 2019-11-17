from django.db import models


class CustomBaseModel(models.Model):
    '''A base model customization.'''

    class Meta:
        abstract=True
    
    def full_clean(self):
        # Remove leading or trailing spaces from strings
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(self, field.name)
                if value != None:
                    setattr(self, field.name, value.strip())

        super().full_clean()

    def save(self, *args, **kwargs):
        # Fields validations run here
        self.full_clean()

        super().save(*args, **kwargs)

    def update(self, **fields):
        # Update and return an object

        for key, value in fields.items():
            setattr(self, key, value)

        self.save()

        return self
