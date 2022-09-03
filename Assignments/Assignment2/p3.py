"""
Your cheapest ride.

You are given a non-empty list of vehicles, you are to find the CHEAPEST vehicle that 
satisfies a list of REQUIREMENTS:
    - need to travel across a given distance
    - need to carry a given load
    - need to arrive within a given time limit

Cost of a vehicle is purely calculated by the amount of money paid for fuel.

For each vehicle, you will be given this information:
    - name: unique identifier for each vehicle (string)
    - capacity: the maximum weigt (in kg) this vehicle can carry (integer)

However, not all vehicles are of the same type. We have 3 types of vehicles (Motorbike, 
Sedan, Truck) with its own characteristics:

[Motorbike]
- fuel cost is 120 Rupiah per km travelled
- average speed when carrying N kg: 50 - (N/10)

[Sedan]
- fuel cost is 200 Rupiah per km travelled
- average speed when carrying N kg: 60 - (N/25)

[Truck]
- fuel cost is 400 Rupiah per km travelled
- average speed when carrying N kg: 45 - (N/100)

These are the following things you need to do:
1. Complete missing attributes/methods for each class
2. Implement the main logic in function best_vehicle with the following arguments:
    - vehicles: list of unique vehicles, can be different type 
    - distance: exact distance (in km) that the vehicle needs to travel (string)
    - load: maximum weight (in kg) the vehicle needs to carry (integer)
    - time_limit: maximum amount of time (in hours) that the vehicle needs to arrive in the
        destination (float)
3. Return the answer with the name of the vehicle.
    
Notes:
    - Select "cheapest" vehicle based on total fuel cost for each case
    - when calculating the time for a vehicle to travel from A to B, use the distance
      and "average speed" (check detailed descriptions for each vehicle)
    - if no vehicles satisfy the requirements, return "Impossible"
    - if there are multiple vehicles that satisfy the requirements, choose the one with the
        maximum capacity (guaranteed will be unique).

Examples
----------------------------------------------------------------------------------------------
Vehicles: 
    - v1: Motorbike("M1", capacity=40)
    - v2: Sedan("Ruby", capacity=200)
    - v3: Truck("Kargo", capacity=2000)

Input:
    vehicles: [v1, v2, v3]

Query: cheapest_ride(vehicles, distance=100, load=100, time_limit=2)
Output: "Ruby"  
Explanation: Based on the load requirements, only "Ruby" and "Kargo" can carry the load.
    Side-by-side comparison when traveling 100km:
    - "Ruby"
        - average speed: 60 - (100/25) = 56 km/hr
        - time = distance/average speed = 100/56 = 1.78 hour
    - "Kargo"
        - average speed: 45 - (100/100) = 44 km/hr
        - time = distance/average speed = 100/39 = 2.56 hour
    Since the time limit is 2 hour, then only "Ruby" satisfy all the requirements.

Query: cheapest_ride(vehicles, distance=100, load=180, time_limit=3)
Output: "Ruby"  
Explanation: Same problem except now the time limit is 3 hour. This means both "Ruby"
    and "Kargo" satisfy the requirements. Now let's compare which one is cheapest:
    - "Ruby": 100 km * 200 Rupiah/km = 20,000 Rupiah
    - "Kargo": 100km * 400 Rupiah/km = 40,000 Rupiah 
    Since "Ruby" is the cheaper option, then it is the answer for this case.

Query: cheapest_ride(vehicles, distance=10, load=5, time_limit=0.5)
Output: "M1"  
Explanation: Load is very light and all vehicles can carry them. Side-by-side comparison:
    - "M1"
        - average speed: 50 - (5/10) = 49.5 km/hr
        - time = distance/average speed = 10/49.5 ~ 0.202 hour
        - cost: 10 km * 120 Rupiah/km = 1200 Rupiah
    - "Ruby"
        - average speed: 60 - (5/25) = 59.8 km/hr
        - time = distance/average speed = 10/59.8 ~ 0.167 hour
        - cost: 10 km * 200 Rupiah/km = 2000 Rupiah
    - "Kargo"
        - average speed: 45 - (5/100) = 44.95 km/hr
        - time = distance/average speed = 10/44.95 = 0.222 hour
        - cost: 10 km * 400 Rupiah/km = 4000 Rupiah
    All vehicles can travel on-time (under 0.5 hour), so we choose the cheapest one (M1).

Query: cheapest_ride(vehicles, distance=10, load=5, time_limit=0.1)
Output: "Impossible"
Explanation: Same problem as previous except now the time_limit is reduced to 0.1. Since
    none of the vehicles can travel under 0.1 hour, we return "Impossible" as the answer.

"""
from typing import List


class Vehicle:
    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity

    # HINT:
    # For each child class, you want to have:
    # - a method to calculate speed, given the load to carry
    # - a method to calculate total cost, given a distance to travel
    #
    # you can apply the concept of inheritance to simplify the implementation

    def time(self, distance, average_speed):
        return distance/average_speed


class Motorbike(Vehicle):
    def fuel_cost(self, distance):
        return 120 * distance

    def average_speed(self, load):
        return 50 - (load/10)


class Sedan(Vehicle):
    def fuel_cost(self, distance):
        return 200 * distance

    def average_speed(self, load):
        return 60 - (load/25)


class Truck(Vehicle):
    def fuel_cost(self, distance):
        return 400 * distance

    def average_speed(self, load):
        return 45 - (load/100)


def cheapest_ride(
    vehicles: List[Vehicle], distance: int, load: int, time_limit: float
) -> str:
    # ----------------------------------- SOLUTION 1 -----------------------------------
    # cost, name, capacity = [], [], []
    # for vehicle in vehicles:
    #     if (vehicle.average_speed(load) != 0) and (vehicle.time(distance, vehicle.average_speed(load)) <= time_limit) and (vehicle.time(distance, vehicle.average_speed(load)) > 0) and (vehicle.capacity >= load):
    #         cost.append(vehicle.fuel_cost(distance))
    #         name.append(vehicle.name)
    #         capacity.append(vehicle.capacity)
    # if len(name) < 1: return "Impossible"
    # elif len(name) == 1: return name[0]
    # else:
    #     capacity_based_cost = [capacity[i] for i in range(len(cost)) if cost[cost.index(min(cost))] == cost[i]]
    #     if len(capacity_based_cost) > 1: return name[capacity.index(max(capacity_based_cost))]
    #     else: return name[cost.index(min(cost))]


    # ----------------------------------- SOLUTION 2 -----------------------------------
    # val = []
    # cheapest = [[vehicle.fuel_cost(distance), vehicle.name, vehicle.capacity] for vehicle in vehicles if (vehicle.average_speed(load) != 0) and (vehicle.time(distance, vehicle.average_speed(load)) <= time_limit) and (vehicle.time(distance, vehicle.average_speed(load)) > 0) and (vehicle.capacity >= load)]
    # if len(cheapest) < 1: return "Impossible"
    # elif len(cheapest) == 1: return cheapest[0][1]
    # else:
    #     capacity_based_cost = [val[2] for val in cheapest if min([val[0] for val in cheapest]) == val[0]]
    #     if len(capacity_based_cost) > 1: val = [val[1] for val in cheapest if (max(capacity_based_cost) == val[2]) and (min([val[0] for val in cheapest]) == val[0])]
    #     else: val = [val[1] for val in cheapest if min([val[0] for val in cheapest]) == val[0]]
    # return val[0]

    # ---------------------------- READABLE FOR SOLUTION 2 -----------------------------
    val = []

    cheapest = [
        [
            vehicle.fuel_cost(distance),
            vehicle.name,
            vehicle.capacity
        ]
        for vehicle in vehicles
        if (
            vehicle.average_speed(load) != 0
            ) and (
                vehicle.time(distance, vehicle.average_speed(load)) <= time_limit
                ) and (
                    vehicle.time(distance, vehicle.average_speed(load)) > 0
                    ) and (
                        vehicle.capacity >= load
                        )
    ]

    if len(cheapest) < 1:
        return "Impossible"
    elif len(cheapest) == 1:
        return cheapest[0][1]
    else:
        capacity_based_cost = [
            val[2]
            for val in cheapest
            if min([val[0] for val in cheapest]) == val[0]
        ]

        if len(capacity_based_cost) > 1:
            val = [
                val[1]
                for val in cheapest
                if (
                    max(capacity_based_cost) == val[2]
                    ) and (
                        min([val[0] for val in cheapest]) == val[0]
                        )
            ]
        else:
            val = [
                val[1]
                for val in cheapest
                if min([val[0] for val in cheapest]) == val[0]
            ]

    return val[0]


# Test your code by uncommenting the following code and modify accordingly
# vehicles = [
#     Motorbike("M1", capacity=40),
#     Sedan("Ruby", capacity=200),
#     Truck("Kargo", capacity=2000),
# ]
# print(cheapest_ride(vehicles, distance=100, load=100, time_limit=2))
# print(cheapest_ride(vehicles, distance=100, load=180, time_limit=3))
#
# vehicles = [
#     Motorbike("Rouge", 100),
#     Sedan("Bellamy", 80),
#     Truck("Dragon", 1000)
# ]
# print(cheapest_ride(vehicles, distance=40, load=100, time_limit=0.99))  # Dragon   --> Bellamy
#
# and then run the following comand
#       python3.9 p3.py
# from within folder Assignment 2
