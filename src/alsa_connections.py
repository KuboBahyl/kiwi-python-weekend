from requests_html import HTMLSession
from redis import StrictRedis
from src import redis_config
# from pprint import pprint
# from time import time

from data_loading import load_data


def search_results(user_dep, user_dest, user_time_dep, user_passengers):
    # time_start = time()
    session = HTMLSession()
    redis_db = StrictRedis(socket_connect_timeout=3, **redis_config)
    return load_data(session, redis_db, user_dep, user_dest, user_time_dep, user_passengers)

    # print("Printing results for {0} passengers, travelling from {1} to {2} at {3}"
    #       .format(user_passengers, user_dep, user_dest, user_time_dep))
    # pprint(results)
    # print("Time of execution: {}".format(time() - time_start))
