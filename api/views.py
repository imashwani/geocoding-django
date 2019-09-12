from django.shortcuts import render, reverse, redirect
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
        location_name = process_location_input_query(location_name)

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


def process_location_input_query(location_name):
    # Assumptions: considering that the user has inserted the address and the city is at the end of the string
    return location_name.replace(",", " ").strip().lower()


# location_name is the query from the user
def get_geocoding(location_name):
    print("caaling ashwani")
    location = Location()
    is_from_cached = False

    if cache.__contains__(location_name):
        is_from_cached = True
        location = cache.get(location_name)
        print("from cache: " + str(location))
    else:
        location = city_match_from_cache(location_name)
        is_from_cached = True
        if location is None:
            # if query was not in the list of city in cache
            # get data from api
            is_from_cached = False
            location = get_from_api(location_name)
            cache.set(location_name, location, timeout=None)

            if location is None:
                return None, is_from_cached
            else:
                print("from api: " + str(location))

    return location, is_from_cached


def city_match_from_cache(location_name):
    for cache_key in cache.keys('*'):
        location_obj = cache.get(cache_key)
        if location_obj != None:
            city = location_obj.city
            if location_name.find(city) != -1:
                print("data from city cache")
                return location_obj
        else:
            return None


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
        address_array = formatted_address.split(',')
        city = address_array[-3].lower() if len(address_array) >= 3 else address_array[-2].lower()

        location.address = location_name
        location.formatted_address = formatted_address
        location.lat = latitude
        location.lng = longitude
        location.city = city
    else:
        return None

    return location


def clear_whole_cache(request):
    # flush all the data from redis cache
    for cache_key in cache.keys('*'):
        cache.set(cache_key, " ", timeout=0)
        print("removing " + cache_key + " from cache")
    return redirect("/")
