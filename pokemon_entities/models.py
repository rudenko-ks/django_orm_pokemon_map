from django.db import models
from django.utils.timezone import now


class Pokemon(models.Model):

    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'{self.title}'


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField(default=now)
    disappeared_at = models.DateTimeField(default=now)
    level = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)
