from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='media', null=True)

    def __str__(self) -> str:
        return f'{self.title}'
