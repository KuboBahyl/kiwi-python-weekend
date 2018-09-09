import pandas as pd


# search for flights within subtree
def make_subtree(flight: str, flights: pd.DataFrame):
    sub_tree = {}
    row = flights[flights['flight_number'] == flight]
    time_now, airport_now = row[['arrival', 'destination']].values[0]
    flights_future = flights[flights['departure'] >= time_now + 60*60]
    flights_now = flights_future[flights_future['departure'] <= time_now + 4*60*60]

    if len(flights_now) == 0 or airport_now not in flights_now['source'].values:
        return sub_tree
    else:
        airport_flights_now = flights_now['flight_number'][ flights_now['source'] == airport_now ]
        for flight_now in airport_flights_now:
            sub_tree[flight_now] = make_subtree(flight_now, flights_future)

        return sub_tree


# search for flights combination
def make_tree(flights: pd.DataFrame, num_bags=0):
    tree = {}
    airports = flights['source'].unique()

    for airport in airports:
        tree[airport] = {}
        airport_flights = flights['flight_number'][(flights['source'] == airport) & \
                                                   (flights['bags_allowed'] >= num_bags)]

        for flight in airport_flights:
            sub_tree = make_subtree(flight, flights)
            tree[airport][flight] = sub_tree

    return tree


# assuming there are no more than 2 stopovers
def search_combinations(tree: dict):
    combinations_all = []
    for airport in tree:
        for flight in tree[airport]:
            combination = [flight]
            combinations_all += [combination]

            for flight_next in tree[airport][flight]:
                combination_next = [flight_next]
                combinations_all += [combination_next]
                combinations_all += [combination + combination_next]

                for flight_next_next in tree[airport][flight][flight_next]:
                    combination_next_next = [flight_next_next]
                    combinations_all += [combination_next_next]
                    combinations_all += [combination_next + combination_next_next]
                    combinations_all += [combination + combination_next + combination_next_next]

    return combinations_all