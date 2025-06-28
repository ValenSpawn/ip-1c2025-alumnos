# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages()
    favourite_list = services.getAllFavouritesByUser(request.user) if request.user.is_authenticated else []
      
    for card in images:
        if 'grass' in card.types:
            card.color = 'border-success'
        elif 'fire' in card.types:
            card.color = 'border-danger'
        elif 'water' in card.types:
            card.color = 'border-primary'
        else:
            card.color = 'border-warning'

    favourite_names = [card.name for card in favourite_list]

    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list,
        'favourite_names': favourite_names
})

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '').strip()
    images = services.getAllImages()
    favourite_list = services.getAllFavouritesByUser(request.user) if request.user.is_authenticated else []
  
    if name:
        images = [card for card in images if name.lower() in card.name.lower()]

    for card in images:
        if 'grass' in card.types:
            card.color = 'border-success'
        elif 'fire' in card.types:
            card.color = 'border-danger'
        elif 'water' in card.types:
            card.color = 'border-primary'
        else:
            card.color = 'border-warning'

    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list
    })
   

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    poke_type = request.POST.get('type', '').strip()
    images = services.getAllImages()
    favourite_list = services.getAllFavouritesByUser(request.user) if request.user.is_authenticated else []

    if poke_type:
        # Filtrar imágenes por tipo
        images = [card for card in images if poke_type in card.types]

        # Asignar color según el tipo
        for card in images:
            if 'grass' in card.types:
                card.color = 'border-success'
            elif 'fire' in card.types:
                card.color = 'border-danger'
            elif 'water' in card.types:
                card.color = 'border-primary'
            else:
                card.color = 'border-warning'

        return render(request, 'home.html', {
            'images': images,
            'favourite_list': favourite_list
        })

    return redirect('home')
    

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    user = request.user
    favourites = services.getAllFavouritesByUser(user)

    return render(request, 'favourites.html', {
        'favourite_list': favourites
    })

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        from .layers.utilities import translator

        user = request.user
        card = translator.fromTemplateIntoCard(request)

        services.saveFavourite(card, user)

        return redirect('home')

@login_required
def deleteFavourite(request):
      if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        services.deleteFavourite(name, user)

        return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('home')
