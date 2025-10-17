from pulp import LpProblem

from business.facility_location import FacilityLocation
from optimization.variables import set_open_facility_variables, set_assign_facility_to_customer_variables


def test__set_open_facility_variables__on_3_facilities__creates_3_variables():
    # ARRANGE
    model = LpProblem("uflp_test", 1)
    facility_location = FacilityLocation(
        num_facilities=3,
        num_customers=2,
        facilities_fixed_cost=[10, 10, 10],
        facilities_location=[(1, 1), (2, 2), (3, 3)],
        customers_location=[(4, 5), (5, 6)],
    )

    # ACT
    set_open_facility_variables(model, facility_location)

    # ASSERT
    assert len(model.y) == 3, f"Expected 3 facility opening variables, but got: " + str(len(model.y))
    assert set(range(3)) == set(model.y.keys()), f"Expected facility opening variable keys to be {set(range(3))}, but got: " + str(set(model.y.keys()))
    for var in model.y.values(): # variable properties are ok
        assert var.lowBound == 0, f"Expected lowBound to be 0, but got: {var.lowBound}"
        assert var.upBound == 1, f"Expected upBound to be 1, but got: {var.upBound}"
        assert var.cat == "Integer", f"Expected cat to be 'Integer', but got: {var.cat}"


def test__set_assign_facility_to_customer_variables__on_3_facilities_2_customers__creates_6_variables():
    # ARRANGE
    model = LpProblem("uflp_test", 1)
    facility_location = FacilityLocation(
        num_facilities=3,
        num_customers=2,
        facilities_fixed_cost=[10, 10, 10],
        facilities_location=[(1, 1), (2, 2), (3, 3)],
        customers_location=[(4, 5), (5, 6)],
    )
    expected_keys = {(f, c) for f in range(3) for c in range(2)}

    # ACT
    set_assign_facility_to_customer_variables(model, facility_location)

    # ASSERT
    assert len(model.x) == 6 # size is ok
    assert expected_keys == set(model.x.keys()) # indices are ok
    for var in model.x.values(): # variable properties are ok
        assert var.lowBound == 0
        assert var.upBound == 1
        assert var.cat == "Integer"