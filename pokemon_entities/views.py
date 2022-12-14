import folium

from django.shortcuts import get_object_or_404, render
from django.utils.timezone import localtime

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent')


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now = localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=now,
                                                    disappeared_at__gte=now)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        if pokemon_entity.pokemon.photo:
            add_pokemon(
                folium_map, pokemon_entity.lat, pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.photo.url))
        else:
            add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon)

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        if pokemon.photo:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': request.build_absolute_uri(pokemon.photo.url),
                'title_ru': pokemon.title,
            })
        else:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title,
            })

    return render(request,
                  'mainpage.html',
                  context={
                      'map': folium_map._repr_html_(),
                      'pokemons': pokemons_on_page,
                  })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    requested_pokemon = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
    }
    if pokemon.photo:
        requested_pokemon['img_url'] = request.build_absolute_uri(
            pokemon.photo.url)

    if pokemon.previous_evolution:
        requested_pokemon['previous_evolution'] = {
            'pokemon_id':
                pokemon.previous_evolution.id,
            'img_url':
                request.build_absolute_uri(pokemon.previous_evolution.photo.url
                                          ),
            'title_ru':
                pokemon.previous_evolution.title,
        }

    if next_evolutions := pokemon.next_evolutions.first():
        requested_pokemon['next_evolution'] = {
            'pokemon_id': next_evolutions.id,
            'img_url': request.build_absolute_uri(next_evolutions.photo.url),
            'title_ru': next_evolutions.title,
        }

    now = localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = pokemon.entities.filter(appeared_at__lte=now,
                                               disappeared_at__gte=now)
    for pokemon_entity in pokemon_entities:
        if pokemon_entity.pokemon.photo:
            add_pokemon(
                folium_map, pokemon_entity.lat, pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.photo.url))
        else:
            add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon)

    return render(request,
                  'pokemon.html',
                  context={
                      'map': folium_map._repr_html_(),
                      'pokemon': requested_pokemon
                  })
