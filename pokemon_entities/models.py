from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='media', null=True)

    def __str__(self) -> str:
        return f'{self.title}'


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    Pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
