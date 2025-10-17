import pulp
from pulp import LpProblem

from business.facility_location import FacilityLocation


def set_objective(model: LpProblem, instance: FacilityLocation):
    """
    Sets the objective function for the facility location problem.
    """
    facility_costs = get_facility_costs(model, instance)
    model.objective_facility_costs = facility_costs  # Store for later reference
    transport_costs = get_transport_costs(model, instance)
    model.objective_transport_costs = transport_costs  # Store for later reference
    model += facility_costs + transport_costs, "Total_Costs"


def get_facility_costs(model: LpProblem, instance: FacilityLocation):
    """
    Retrieves the facility opening costs:

        ∑(f ∈ F) y_f * h_f

    Where:
    - F is the set of facilities
    - y_f  is a binary variable that is 1 if facility f is opened, and 0 otherwise
    - h_f is the fixed cost of opening facility f
    """
    return pulp.lpSum(
        instance.facilities_fixed_cost[f] * model.y[f]
        for f in range(instance.num_facilities)
    )

def get_transport_costs(model: LpProblem, instance: FacilityLocation):
    """
    Sets the transportation costs in the objective function:

        ∑(f ∈ F) ∑(c ∈ C) x_fc * d(f, c)

    Where:
    - F is the set of facilities
    - C is the set of customers
    - x_fc is a binary variable that is 1 if facility f serves customer c, and 0 otherwise
    - d(f, c) is the distance between facility f and customer c
    """

    return pulp.lpSum(
        instance.get_distance(f, c) * model.x[(f, c)]
        for f in range(instance.num_facilities)
        for c in range(instance.num_customers)
    )