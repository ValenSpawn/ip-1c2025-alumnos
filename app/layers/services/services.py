# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

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
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.
        filtered_cards.append(card)

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(card, user):
    card.user = user
    return repositories.save_favourite(card)

# usados desde el template 'favourites.html'
def getAllFavouritesByUser(user):
    if not user.is_authenticated:
        return []

    raw_favourites = repositories.get_all_favourites(user)
    mapped_favourites = []

    for fav in raw_favourites:
        card = translator.fromDictionaryIntoCard(fav)  # ← adaptá el nombre si es necesario
        mapped_favourites.append(card)

    return mapped_favourites
    

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)
