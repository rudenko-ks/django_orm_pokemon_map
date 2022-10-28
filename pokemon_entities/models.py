from email.policy import default
from django.db import models
from django.utils.timezone import now


class Pokemon(models.Model):

    title = models.CharField(max_length=200, verbose_name='Название')
    title_en = models.CharField(max_length=200,
                                blank=True,
                                verbose_name='Название, англ.')
    title_jp = models.CharField(max_length=200,
                                blank=True,
                                verbose_name='Название, яп.')
    photo = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='next_evolutions',
        verbose_name='Из кого эволюционировал')

    def __str__(self) -> str:
        return f'{self.title}'


class PokemonEntity(models.Model):
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.CASCADE,
                                related_name='entities',
                                verbose_name='Покемон')
    appeared_at = models.DateTimeField(null=True,
                                       blank=True,
                                       verbose_name='Время появления')
    disappeared_at = models.DateTimeField(null=True,
                                          blank=True,
                                          verbose_name='Время исчезновения')
    level = models.IntegerField(blank=True, verbose_name='Уровень')
    health = models.IntegerField(blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(blank=True, verbose_name='Сила')
    defense = models.IntegerField(blank=True, verbose_name='Защита')
    stamina = models.IntegerField(blank=True, verbose_name='Выносливость')
