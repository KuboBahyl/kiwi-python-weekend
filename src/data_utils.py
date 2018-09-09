import csv
import sys
import pandas as pd
from datetime import datetime
from time import mktime


# Data loading from stdin
def stdin_flights() -> pd.DataFrame:
    f = sys.stdin.read().splitlines()
    lines = list(csv.reader(f))
    column_names = lines[0]
    data = lines[1:]
    num_rows = len(data)

    # filling DF with data
    flights = pd.DataFrame(columns=column_names)
    for i in range(num_rows):
        flights.loc[i] = data[i]

    # convert to numeric cols
    numeric_columns = ['price', 'bags_allowed', 'bag_price']
    flights[numeric_columns] = flights[numeric_columns].apply(pd.to_numeric)

    return flights


# Preprocessing
def preprocess(flights: pd.DataFrame):

    def date2timestamp(date: str):
        return mktime(datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").timetuple())

    flights['departure'] = flights['departure'].apply(lambda x: date2timestamp(x))
    flights['arrival'] = flights['arrival'].apply(lambda x: date2timestamp(x))
    return flights
