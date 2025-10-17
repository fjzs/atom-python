from pulp import LpProblem, LpVariable
from business.facility_location import FacilityLocation


def set_variables(model: LpProblem, instance: FacilityLocation) -> None:
    """
    Define the decision variables for the optimization model.

    Parameters:
    - model: The PuLP LpProblem instance where variables will be added.
    - instance: The FacilityLocation instance containing problem data.
    """
    set_open_facility_variables(model, instance)
    set_assign_facility_to_customer_variables(model, instance)


def set_open_facility_variables(model: LpProblem, instance: FacilityLocation):
    """
    Define the facility opening decision variables for the optimization model:

    y_f (binary) ∀ f ∈ F

    Where:
    - F is the set of facilities
    """

    # Note: When you create a variable using LpVariable, it does not automatically get added to the model.
    # Instead, variables are associated with the model when they are used in constraints or the objective function.
    # For convenience, we attach them directly to the model object here.
    model.y = LpVariable.dicts(
        "open_facility",
        list(range(instance.num_facilities)),  # don't use range because it creates an iterator, to test we need a list
        lowBound=0,
        upBound=1,
        cat="Integer" # Internally pulp with denote this var as 'Integer'
    )

    # # BUG 1: Replace the code above with the code below to see the unit test fail
    # model.y = LpVariable.dicts(
    #     "open_facility",
    #     list(range(instance.num_facilities + 1)), # Introduced a bug by adding +1
    #     lowBound=0,
    #     upBound=1,
    #     cat="Integer"
    # )


def set_assign_facility_to_customer_variables(model: LpProblem, instance: FacilityLocation):
    """
    Define the customer assignment decision variables for the optimization model.

    x_fc (binary) ∀ f ∈ F, c ∈ C

    Where:
    - F is the set of facilities
    - C is the set of customers
    """

    # Note: When you create a variable using LpVariable, it does not automatically get added to the model.
    # Instead, variables are associated with the model when they are used in constraints or the objective function.
    # For convenience, we attach them directly to the model object here.
    model.x = LpVariable.dicts(
        "assign_facility_to_customer",
        [(f, c) for f in range(instance.num_facilities) for c in range(instance.num_customers)],
        lowBound=0,
        upBound=1,
        cat="Integer" # Internally pulp with denote this var as 'Integer'
    )
