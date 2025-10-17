import random
from business.facility_location import FacilityLocation

# Grid boundaries
GRID_SIZE = 100
MIN_FIXED_COST = 100
MAX_FIXED_COST = 100


def create_random_instance(num_facilities: int, num_customers: int) -> FacilityLocation:
    """
    Create a random instance of the facility location problem
    with coordinates in a GRID_SIZE x GRID_SIZE grid and random fixed costs.

    Args:
        num_facilities: number of facilities
        num_customers: number of customers
    """

    facilities_fixed_cost = [
        random.randint(MIN_FIXED_COST, MAX_FIXED_COST) for _ in range(num_facilities)
    ]
    facilities_location = [
        (random.randint(1, GRID_SIZE - 1), random.randint(1, GRID_SIZE - 1))
        for _ in range(num_facilities)
    ]
    customers_location = [
        (random.randint(1, GRID_SIZE - 1), random.randint(1, GRID_SIZE - 1))
        for _ in range(num_customers)
    ]

    return FacilityLocation(
        num_facilities=num_facilities,
        num_customers=num_customers,
        facilities_fixed_cost=facilities_fixed_cost,
        facilities_location=facilities_location,
        customers_location=customers_location,
    )
