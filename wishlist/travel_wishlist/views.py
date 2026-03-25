'''
controllers are called views in django
'''


from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages


@login_required
def place_list(request):

    if request.method == "POST":
        form = NewPlaceForm(request.POST)  # creating a form from data in the request
        place = form.save(commit=False)  # creating a model object from form
        place.user = request.user
        if form.is_valid():  # validation against db constraints
            place.save()  # saves place to db
            return redirect('place_list')  # reload homepage

    # if not a POST or form is not valid, render page with form to add new place and list places
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()  # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})


def about(request):
    about = 'a website to create a wishlist of places'
    return render(request, 'travel_wishlist/about.html', {'author': 'Somi', 'about': about})


@login_required
def places_visited(request):
    visited_places = Place.objects.filter(visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', {'visited_places': visited_places})


@login_required
def place_was_visited(request, place_pk):  # place_pk is from url path (needs to match)
    if request.method == "POST":
        #place = Place.objects.get(pk=place_pk)  # 'pk' is db column, 'place_pk' is from argument
        place = get_object_or_404(Place, pk=place_pk)  # will return 404 if object not found
        if place.user == request.user:
            place.visited = True  # directly manage field in model object
            place.save()  # save to db
        else:
            return HttpResponseForbidden()

    # return redirect('places_visited)
    return redirect('place_list')  # 'place_list' is path from urls.py


@login_required
def place_details(request,place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    # does place belong to current user
    if place.user != request.user:
        return HttpResponseForbidden()

    # is this GET or POST request?

    # if POST, validate form and update
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)  # new TripReviewForm form object from the data that was sent with the HTTP request; put in data the user has sent to update an instance from the model db
        if form.is_valid():  # are all the fields filled in that are required by the db with the right type of data
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)
        return redirect('place_details', place_pk=place_pk)

    # if GET, show Place info and form
    else:
        # if place is visited, show form
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()

