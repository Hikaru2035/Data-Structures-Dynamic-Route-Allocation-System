city_coordinates = {
    "Hanoi": (105.8542, 21.0285),
    "Da Nang": (108.2068, 16.0471),
    "Nha Trang": (109.1967, 12.2388),
    "Dalat": (108.4582, 11.9404),
    "Hai Phong": (106.6881, 20.8449),
    "HCMC": (106.6297, 10.8231)
}

def distances_between_two_cities(first_city, second_city):
    x1, y1 = city_coordinates[first_city]
    x2, y2 = city_coordinates[second_city]
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def route_distance(route):
    distance = 0
    for i in range(len(route) - 1):
        distance += distances_between_two_cities(route[i], route[i + 1])
    distance += distances_between_two_cities(route[-1], "Hanoi")
    return distance

def permutations_generated(elements):
    if len(elements) == 0:
        return [[]]
    
    permutations = []

    for i in range(len(elements)):
        rest = elements[:i] + elements[i + 1:]
        for each in permutations_generated(rest):
            permutations.append([elements[i]] + each)
    
    return permutations

def generate_brute_force_route(starting_point="Hanoi"):
    print("Dalat, Da Nang, HCMC, Nha Trang, Hai Phong")
    print("Enter the cities to delivery route (comma-separated):")
    destinations = input().strip().split(",")
    destinations = [city.strip() for city in destinations if city.strip()]
    
    if starting_point in destinations:
        destinations.remove(starting_point)
    
    all_routes = permutations_generated(destinations)
    
    optimal_route = None
    min_distance = float('inf')
    for route in all_routes:
        curr_route = [starting_point] + route
        curr_distance = route_distance(curr_route)
        if curr_distance < min_distance:
            min_distance = curr_distance
            optimal_route = curr_route
    
    return optimal_route, min_distance


route, distance = generate_brute_force_route()
print("\nOptimal Route:", " -> ".join(route))
print("Total Distance:", round(distance, 2), "units")
