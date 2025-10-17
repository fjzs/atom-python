import pytest
from pulp import LpProblem

from business.facility_location import FacilityLocation
from model_comparer.comparator import are_expressions_equal
from optimization.objective_function import get_facility_costs, get_transport_costs
from optimization.variables import set_variables


@pytest.fixture
def setup():
    # Setup logic here
    model = LpProblem("uflp_test", 1)
    facility_location = FacilityLocation(
        num_facilities=2,
        num_customers=2,
        facilities_fixed_cost=[10, 20],
        facilities_location=[(1, 1), (4, 2)],
        customers_location=[(4, 1), (1, 6)],
    )
    set_variables(model, facility_location)
    return model, facility_location


def test__get_facility_costs__on_2_facilities__sets_it_correctly(setup):
    # ARRANGE
    model, facility_location = setup
    expected_expression = 10 * model.y[0] + 20 * model.y[1]

    # ACT
    actual_expression = get_facility_costs(model, facility_location)

    # ASSERT
    assert are_expressions_equal(expected_expression, actual_expression)


def test__get_transport_costs__on_2_facilities_2_customers__sets_it_correctly(setup):
    # ARRANGE
    model, facility_location = setup
    expected_expression = (facility_location.get_distance(0,0) * model.x[(0, 0)] +
                           facility_location.get_distance(0,1) * model.x[(0, 1)] +
                           facility_location.get_distance(1,0) * model.x[(1, 0)] +
                           facility_location.get_distance(1,1) * model.x[(1, 1)])

    # ACT
    actual_expression = get_transport_costs(model, facility_location)

    # ASSERT
    assert are_expressions_equal(expected_expression, actual_expression)