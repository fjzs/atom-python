import pytest

from business.facility_location import FacilityLocation


def test_get_distance_given1customer1facility_computes_euclidean_distance():
    # Arrange
    facility_location = FacilityLocation(
        num_facilities=1,
        num_customers=1,
        facilities_fixed_cost=[0],
        facilities_location=[(1, 1)],
        customers_location=[(4, 5)],
    )

    # Act
    distance = facility_location.get_distance(0, 0)

    # Assert
    assert distance == pytest.approx(5)


def test_get_distance_given_wrong_facility_index_raises_exception():
    # Arrange
    facility_location = FacilityLocation(
        num_facilities=1,
        num_customers=1,
        facilities_fixed_cost=[0],
        facilities_location=[(1, 1)],
        customers_location=[(4, 5)],
    )

    # Act & Assert
    with pytest.raises(IndexError):
        facility_location.get_distance(facility_index=1, customer_index=0)


def test_get_distance_given_wrong_customer_index_raises_exception():
    # Arrange
    facility_location = FacilityLocation(
        num_facilities=1,
        num_customers=1,
        facilities_fixed_cost=[0],
        facilities_location=[(1, 1)],
        customers_location=[(4, 5)],
    )

    # Act & Assert
    with pytest.raises(IndexError):
        facility_location.get_distance(facility_index=0, customer_index=1)
