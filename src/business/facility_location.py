from pydantic import BaseModel, Field, model_validator
from typing import List, Tuple
import math
from pathlib import Path


class FacilityLocation(BaseModel):
    """
    Represents an uncapacitated facility location problem.
    """

    num_facilities: int = Field(
        ..., gt=0, description="Number of facilities must be > 0"
    )
    num_customers: int = Field(..., gt=0, description="Number of customers must be > 0")
    facilities_fixed_cost: List[float] = Field(
        ..., description="Fixed cost of opening each facility"
    )
    facilities_location: List[Tuple[int, int]] = Field(
        ..., description="List of (x, y) coordinates for facilities"
    )
    customers_location: List[Tuple[int, int]] = Field(
        ..., description="List of (x, y) coordinates for customers"
    )

    @model_validator(mode="after")
    def check_consistency(self):
        # Facilities checks
        if len(self.facilities_fixed_cost) != self.num_facilities:
            raise ValueError(
                f"num_facilities={self.num_facilities} but facilities_fixed_cost has {len(self.facilities_fixed_cost)} elements"
            )
        if len(self.facilities_location) != self.num_facilities:
            raise ValueError(
                f"num_facilities={self.num_facilities} but facilities_location has {len(self.facilities_location)} elements"
            )

        # Customers checks
        if len(self.customers_location) != self.num_customers:
            raise ValueError(
                f"num_customers={self.num_customers} but customers_location has {len(self.customers_location)} elements"
            )
        return self

    def get_distance(self, facility_index: int, customer_index: int) -> float:
        """
        Calculate the Euclidean distance between a facility and a customer.
        """
        if not (0 <= facility_index < self.num_facilities):
            raise IndexError(f"Facility index {facility_index} out of bounds")

        if not (0 <= customer_index < self.num_customers):
            raise IndexError(f"Customer index {customer_index} out of bounds")

        fx, fy = self.facilities_location[facility_index]
        cx, cy = self.customers_location[customer_index]
        distance = math.hypot(fx - cx, fy - cy)
        return round(distance, 1)  # for simplicity

    def save_to_json(self, folder_path: Path, filename: str = "data.json") -> None:
        """
        Save the FacilityLocation instance as a JSON file.

        Args:
            folder_path (Path): Path to the folder where the file will be saved.
            filename (str): Name of the JSON file (default: 'data.json').
        """
        file_path = folder_path / filename

        # Use Pydantic's built-in .model_dump_json() for JSON serialization
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=4))
