from pulp import LpProblem, lpSum

from business.facility_location import FacilityLocation


def assign_customers(model: LpProblem, instance: FacilityLocation) -> None:
    """
    Each customer must be assigned to exactly one facility:

        ∑(f ∈ F) x_fc = 1  ∀ c ∈ C

    Where:
    - F is the set of facilities
    - C is the set of customers
    - x_fc is a binary variable that is 1 if facility f serves customer c, and 0 otherwise
    """
    for c in range(instance.num_customers):
        model += (
            lpSum(model.x[(f, c)] for f in range(instance.num_facilities)) == 1,
            f"AssignCustomer_{c}"
        )

    # # BUG 2: Uncomment the code below to see the unit test fail
    # for c in range(instance.num_customers):
    #     model += (
    #         lpSum(model.x[(f, c)]*2 for f in range(instance.num_facilities)) == 1, # Introduced a bug by multiplying by 2
    #         f"AssignCustomer_{c}"
    #     )


def assigned_customers_imply_open_facility(model: LpProblem, instance: FacilityLocation) -> None:
    """
    A customer can only be served by an opened facility:

        x_fc ≤ y_f  ∀ f ∈ F, c ∈ C

    Where:
    - F is the set of facilities
    - C is the set of customers
    - x_fc is a binary variable that is 1 if facility f serves customer c, and 0 otherwise
    - y_f  is a binary variable that is 1 if facility f is opened, and 0 otherwise
    """
    for f in range(instance.num_facilities):
        for c in range(instance.num_customers):
            model += (
                model.x[(f, c)] <= model.y[f],
                f"OpenFacility_{f}_for_Customer_{c}"
            )