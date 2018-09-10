from urllib.parse import parse_qs, urlparse, urlencode
from boltons import strutils
from requests_html import HTMLSession
import json
import datetime

from src import url_locations, url_template
from postgres_utils import insert_to_pg


def slugify(text: str):
    return strutils.slugify(text, delim='_', lower=True)


def get_locations(session):
    return session.get(url_locations).json()


def get_id(city, locations_json):
    for location in locations_json:
        if location['name'] == city:
            return location['id']

    raise ValueError("Non-existing destination: {}".format(city))


def scrap_asus(session, user_dep, user_dep_id, user_dest, user_dest_id, user_time_dep, user_passengers):
    # build query from template
    query_dict = parse_qs(urlparse(url_template).query)
    for key, value in query_dict.items():
        query_dict[key] = value[0]

    # update query
    query_dict['originStationNameId'] = user_dep
    query_dict['originStationId'] = user_dep_id
    query_dict['destinationStationNameId'] = user_dest
    query_dict['destinationStationId'] = user_dest_id
    query_dict['departureDate'] = user_time_dep.replace('-', '/')
    query_dict['_departureDate'] = user_time_dep.replace('-', '/')
    query_dict['passengerType-1'] = user_passengers

    # create new query string
    query_string = urlencode(query_dict)

    # fetch raw results
    url_results = session \
        .get('https://www.alsa.com/en/web/bus/checkout?', params=query_string).html \
        .find('data-sag-journeys-component', first=True) \
        .attrs['sag-journeys-table-body-url']

    journeys_json = session.get(url_results).json()

    if 'errorMessage' not in journeys_json:
        with open('example_journey.json', 'w') as f:
            json.dump(journeys_json['journeys'][0], f)

        # filter
        results_json = []
        for journey in journeys_json['journeys']:
            results_json.append({'departure_time': journey['departureDataToFilter'],
                                 'arrival_time': journey['arrivalDataToFilter'],
                                 'from': journey['originName'],
                                 'to': journey['destinationName'],
                                 'type': 'bus' if 'busCharacteristic' in journey else 'train',
                                 'price': journey['fares'][0]['price'],
                                 'passengers': user_passengers
                                 })

        return results_json

    else:
        # raise ValueError("No results within these dates")
        return {'message': "Error message occured in results. Check inputs!"}


def load_data(user_dep: str, user_dest: str, user_time_dep: str, user_passengers: int,
              redis_db = None, pg_conn = None) -> list:

    session = HTMLSession()

    if redis_db:
        try:
            user_dep_id = redis_db.get('city_id_' + slugify(user_dep)).decode('utf-8')
            user_dest_id = redis_db.get('city_id_' + slugify(user_dest)).decode('utf-8')

        except:
            locations_json = get_locations(session)
            user_dep_id = get_id(user_dep, locations_json)
            user_dest_id = get_id(user_dest, locations_json)
            redis_db.set('city_id_' + slugify(user_dep), user_dep_id)
            redis_db.set('city_id_' + slugify(user_dest), user_dest_id)

        journey_redis_name = '_'.join(['journey', str(user_dep_id), str(user_dest_id), user_time_dep])

        # return redis_db.get(journey_redis_name).decode('utf-8')
        results_json = scrap_asus(session, user_dep, user_dep_id, user_dest, user_dest_id,
                                  user_time_dep, user_passengers)
        redis_db.set(journey_redis_name, results_json)
        return results_json

    elif pg_conn:

        # TODO try to load data from pg

        locations_json = get_locations(session)
        user_dep_id = get_id(user_dep, locations_json)
        user_dest_id = get_id(user_dest, locations_json)
        results_json = scrap_asus(session, user_dep, user_dep_id, user_dest, user_dest_id,
                                  user_time_dep, user_passengers)

        for result_dict in results_json:




        d = datetime.datetime.now()
        values_test = {'src_id': 91342,
                  'dst_id': 91302,
                  'dep': datetime.datetime(2012, 5, 1),
                  'arr': datetime.datetime(2012, 5, 1),
                  'price': 133.7,
                  'type': 'test'}

        insert_to_pg(pg_conn, values_test)


        # sql_select = "SELECT * FROM connections WHERE price < 100"
        #
        # with pg_conn.cursor(cursor_factory=RealDictCursor) as cursor:
        #     cursor.execute(sql_select)
        #     results_dict = cursor.fetchall()
        #     return results_dict




