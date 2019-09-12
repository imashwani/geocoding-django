Assignment Details:

1. Implemented the im-memory caching using redis in django
2. Api call is made is the data for the query(address/ state) is not present in the cache
3. Response from api is stored in cache, and next time fetched from the cache
4. Also, if the query is full address with city, I search the cache if that city data is already present,
    if so the cached data is used
5. In the model, we are storing lat, lng, Formatted address and city from api response,

Assumptions: The query received is a state or full address of the location.

##
If the received query was not queried before, tried to find the if the city matched with any of the cached data.
Couldn't get time to improve the test_redis.py test cases
##

## How to setup project?

Install redis if not already present
    - sudo apt-get update
    - sudo apt-get install redis-server
    - sudo systemctl enable redis-server.service
check if redis is running in the
    - redis-cli -n 1
    - ping
    you will get response as PONG

Then, clone the repo and run the following commands

cd django
pip install virtualenv
virtualenv env
source env/lib/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver



To run the tests use the following command

python manage.py test


Thank you.