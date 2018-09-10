from redis import StrictRedis
from src import redis_config, pg_config
import psycopg2

from data_loading import load_data


def search_results(user_dep, user_dest, user_time_dep, user_passengers, postgres=False, redis=False):
    redis_db = None
    pg_conn = None

    if redis:
        redis_db = StrictRedis(socket_connect_timeout=3, **redis_config)

    elif postgres:
        pg_conn = psycopg2.connect(**pg_config)

    return load_data(user_dep, user_dest, user_time_dep, user_passengers, redis_db, pg_conn)

    # print("Printing results for {0} passengers, travelling from {1} to {2} at {3}"
    #       .format(user_passengers, user_dep, user_dest, user_time_dep))
    # pprint(results)
    # print("Time of execution: {}".format(time() - time_start))
