import pytest

from business.solution import Solution

def test__sum_of_costs_match_total_cost__no_exception():
    # ACT & ASSERT
    solution = Solution(
        open_facilities=[0, 1],
        customer_assignment=[0, 1, 1],
        facility_costs=100.0,
        transport_costs=50.0,
        total_costs=150.0
    ) # no exception thrown

def test__sum_of_costs_dont_match_total_cost__exception_raised():
    # ACT & ASSERT
    with pytest.raises(ValueError) as excinfo:
        Solution(
            open_facilities=[0, 1],
            customer_assignment=[0, 1, 1],
            facility_costs=120.0,
            transport_costs=50.0,
            total_costs=150.0
        )
