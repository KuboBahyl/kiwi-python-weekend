import pandas as pd


# remove the cases like A -> B -> A -> B
def filter_cycles(combinations: list, flights: pd.DataFrame):
    for combination in combinations:
        if len(combination) >= 3: # able to make cycled route
            routes = []
            for flight in combination:
                row = flights[flights['flight_number'] == flight]
                route = row[['source', 'destination']].values[0]
                if list(route) in routes:
                    combinations.remove(combination)
                    break
                else:
                    routes += [list(route)]

    return combinations


# remove the same flight combinations
def filter_duplicates(combinations: list):
    combinations_unique = set(tuple(x) for x in combinations)
    return [list(x) for x in combinations_unique]


# calculate price for each combination list
def add_prices(combinations: list, flights: pd.DataFrame, num_bags=0):
    num_combination = len(combinations)
    for i in range(num_combination):
        combination_price = 0
        for flight in combinations[i]:
            row = flights[flights['flight_number'] == flight]
            combination_price += row['price'].values[0] + num_bags * row['bag_price'].values[0]

        combinations[i] += [combination_price]

    return combinations