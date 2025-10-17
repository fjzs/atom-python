import pytest
from pulp import LpProblem, LpConstraint, LpConstraintEQ, LpConstraintLE

from business.facility_location import FacilityLocation
from model_comparer.comparator import are_constraints_equal
from optimization.constraints import assign_customers, assigned_customers_imply_open_facility
from optimization.variables import set_variables


@pytest.fixture
def setup():
    # Setup logic here
    model = LpProblem("uflp_test", 1)
    facility_location = FacilityLocation(
        num_facilities=2,
        num_customers=2,
        facilities_fixed_cost=[10, 10],
        facilities_location=[(1, 1), (2, 2)],
        customers_location=[(4, 5), (5, 6)],
    )
    set_variables(model, facility_location)
    return model, facility_location


def test_constraint_assign_customer(setup):
    # ARRANGE
    model, facility_location = setup

    # Expected constraints
    expected_constraints = dict()
    expected_constraints['AssignCustomer_0'] = LpConstraint(
        e=model.x[(0, 0)] + model.x[(1, 0)],
        sense=LpConstraintEQ,
        rhs=1
    )
    expected_constraints['AssignCustomer_1'] = LpConstraint(
        e=model.x[(0, 1)] + model.x[(1, 1)],
        sense=LpConstraintEQ,
        rhs=1
    )

    # Get the number of constraints in the model before adding more
    num_constraints_before = len(model.constraints)

    # ACT
    assign_customers(model, facility_location)
    num_constraints_after = len(model.constraints)

    # Check that the number of new constraints added is as expected
    assert num_constraints_after - num_constraints_before == len(expected_constraints),\
        f"Expected {len(expected_constraints)} new constraints, but got {num_constraints_after - num_constraints_before}"

    # ASSERT
    # Check each expected constraint is in the model
    for key, expected_constraint in expected_constraints.items():
        actual_constraint = model.constraints[key]
        assert are_constraints_equal(expected_constraint, actual_constraint)


def test_assigned_customers_imply_open_facility(setup):
    # ARRANGE
    model, facility_location = setup

    # Expected constraints
    expected_constraints = dict()
    expected_constraints['OpenFacility_0_for_Customer_0'] = LpConstraint(
        e=model.x[(0, 0)] - model.y[0],
        sense=LpConstraintLE,
        rhs=0
    )
    expected_constraints['OpenFacility_0_for_Customer_1'] = LpConstraint(
        e=model.x[(0, 1)] - model.y[0],
        sense=LpConstraintLE,
        rhs=0
    )
    expected_constraints['OpenFacility_1_for_Customer_0'] = LpConstraint(
        e=model.x[(1, 0)] - model.y[1],
        sense=LpConstraintLE,
        rhs=0
    )
    expected_constraints['OpenFacility_1_for_Customer_1'] = LpConstraint(
        e=model.x[(1, 1)] - model.y[1],
        sense=LpConstraintLE,
        rhs=0
    )

    # Get the number of constraints in the model before adding more
    num_constraints_before = len(model.constraints)

    # ACT
    assigned_customers_imply_open_facility(model, facility_location)
    num_constraints_after = len(model.constraints)

    # ASSERT
    # Check that the number of new constraints added is as expected
    assert num_constraints_after - num_constraints_before == len(expected_constraints), \
        f"Expected {len(expected_constraints)} new constraints, but got {num_constraints_after - num_constraints_before}"

    # Check each expected constraint is in the model
    for key, expected_constraint in expected_constraints.items():
        actual_constraint = model.constraints[key]
        assert are_constraints_equal(expected_constraint, actual_constraint)