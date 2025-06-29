# capa de servicio/lógica de negocio
from app.models import Favourite
from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    raw_images = transport.getAllImages()
    cards = []
    for image_data in raw_images:
        card = translator.fromRequestIntoCard(image_data)
        cards.append(card)
    return cards
   

# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        if name.lower() in card.name.lower():
            filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        if type_filter.lower() in [t.lower() for t in card.types]:
            filtered_cards.append(card)

    return filtered_cards

def saveFavourite(card, user):

    if Favourite.objects.filter(user=user, name=card.name).exists():
        return None

    return repositories.save_favourite(card, user)

# usados desde el template 'favourites.html'
def getAllFavouritesByUser(user):
    if not user.is_authenticated:
        return []

    raw_favourites = repositories.get_all_favourites(user)
    mapped_favourites = []

    for fav in raw_favourites:
       card = translator.fromRepositoryIntoCard(fav)
       mapped_favourites.append(card)

    return mapped_favourites
    

def deleteFavourite(name, user):
    try:
        fav = Favourite.objects.get(name=name, user=user)
        fav.delete()
        return True
    except Favourite.DoesNotExist:
        print(f"El favorito '{name}' no existe o no pertenece al usuario.")
        return False

   

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)
