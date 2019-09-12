from django.shortcuts import render, reverse, redirect
from django.http import Http404
from .models import Location
from django.core.cache import cache
from .forms import LocationModelForm
import requests
from .constants import GEOCODE_URL, GEO_CODE_API_KEY

''' @index() function view is served as the home page of the website,
 responsible for all get as well as post request on the page'''


def index(request):
    template = 'api/index.html'
    context = {}
    location_form = LocationModelForm()
    context['location_form'] = location_form
    is_cached = False

    # On submission of form from the index.html
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
        # get the location and where is it data from api or cache
        location_response, is_cached = get_geocoding(location_name)
        context['is_cached'] = is_cached

        if location_response:
            context['location'] = location_response
        context['query'] = location_name

    # to show the cache data on index.html
    all_cache = []
    # tells if cache is empty
    is_cache_empty = True
    all_keys = cache.keys('*')
    if len(all_keys):
        is_cache_empty = False

    for key in all_keys:
        all_cache.append(cache.get(key))

    context['cache'] = zip(all_keys, all_cache)

    context['is_cache_empty'] = is_cache_empty
    return render(request, template, context=context)


# removing , and white spaces
def process_location_input_query(location_name):
    # Assumptions: considering that the user has inserted the address and the city is at the end of the string
    return location_name.replace(",", " ").strip().lower()


# location_name is the query from the user
def get_geocoding(location_name):
    location = Location()
    is_from_cache = False

    if cache.__contains__(location_name):
        is_from_cache = True
        location = cache.get(location_name)
        print("from cache: " + str(location))
    else:
        location = city_match_from_cache(location_name)
        is_from_cache = True
        if location is None:
            # if query was not in the list of city in cache
            # get data from api
            is_from_cache = False
            location = get_from_api(location_name)
            cache.set(location_name, location, timeout=None)

            if location is None:
                # is data received from api has zero results, in case of invalid address
                return None, is_from_cache
            else:
                print("from api: " + str(location))

    return location, is_from_cache


# Check if the city name is present as substring in the query received
def city_match_from_cache(location_name):
    # iterate over all the keys in cache
    for cache_key in cache.keys('*'):
        location_obj = cache.get(cache_key)
        if location_obj != None:
            city = location_obj.city
            if location_name.find(city) != -1:
                # if city is substring of query
                return location_obj
        else:
            return None


# making api call to map.googel.com
def get_from_api(location_name):
    # initialize location object from Model
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
    elif json_response['status'] == "REQUEST_DENIED":
        print("The api request has been denied, with error " + json_response['error_message'])
        return None
    else:
        # Api was unable to get any response
        return None
    return location


# this is used to clear cached data from index.html page
# and redirects back to homepage that is index.html
def clear_whole_cache(request):
    # flush all the data from redis cache
    for cache_key in cache.keys('*'):
        cache.set(cache_key, " ", timeout=0)
        print("removing " + cache_key + " from cache")
    return redirect("/")
