from django.shortcuts import render
from django.http import Http404
from .models import Location
from django.core.cache import cache
from .forms import LocationModelForm
import requests
from .constants import GEOCODE_URL, GEO_CODE_API_KEY


def index(request):
    template = 'api/index.html'
    context = {}
    location_form = LocationModelForm()
    context['location_form'] = location_form
    is_cached = False

    if request.method == 'POST':
        form = LocationModelForm(request.POST)
        location_name = ""
        if form.is_valid():
            location_name = form.cleaned_data['address']
        else:
            raise Http404
        # process location name
        location_name = location_name.replace(",", "").strip().lower()
        if location_name == '' or None:
            return render(request, template, context=context)
        location_response, is_cached = get_geocoding(location_name)
        context['is_cached'] = is_cached

        if location_response:
            context['location'] = location_response
        context['query'] = location_name

    all_cache = []
    is_empty = True
    all_keys = cache.keys('*')
    for key in all_keys:
        is_empty = False
        all_cache.append(cache.get(key))

    context['cache'] = zip(all_keys, all_cache)
    context['is_empty'] = is_empty
    return render(request, template, context=context)


def get_geocoding(location_name):
    location = Location()
    is_cached = False

    if is_location_in_cache(location_name):
        is_cached = True
        location = cache.get(location_name)
        print("from cache: " + str(location))
    else:
        location = get_from_api(location_name)
        if location != None:
            cache.set(location_name, location, timeout=None)
            print("from api: " + str(location))
        else:
            cache.set(location_name, None, timeout=None)
            return None, is_cached

    return location, is_cached


def is_location_in_cache(location_name):
    if cache.__contains__(location_name):
        return True
    return False


def get_from_api(location_name):
    location = Location()
    location.address = location_name
    location.lat = 0.0
    location.lng = 0.0
    PARAMS = {'key': GEO_CODE_API_KEY,
              'address': location_name}
    response = requests.get(url=GEOCODE_URL, params=PARAMS)
    json_response = response.json()
    if json_response['status'] != 'ZERO_RESULTS':
        latitude = json_response['results'][0]['geometry']['location']['lat']
        longitude = json_response['results'][0]['geometry']['location']['lng']
        formatted_address = json_response['results'][0]['formatted_address']

        location.address = location_name
        location.formatted_address = formatted_address
        location.lat = latitude
        location.lng = longitude
    else:
        return None

    return location
