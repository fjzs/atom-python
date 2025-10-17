from pathlib import Path

from pydantic import BaseModel, Field, model_validator
from typing import List


class Solution(BaseModel):
    """
    Represents a solution for the uncapacitated facility location problem.

    Attributes:
        open_facilities: List of facility indices that are opened (0-based).
        customer_assignment: List where the i-th element indicates the
                             facility index to which customer i is assigned.
        facility_costs: Total fixed costs for opening the facilities.
        transport_costs: Total transportation costs for serving the customers.
        total_costs: Total costs.
    """

    open_facilities: List[int] = Field(
        ..., description="Indices of facilities that are opened"
    )
    customer_assignment: List[int] = Field(
        ...,
        description="customer_assignment[i] is the facility index assigned to customer i",
    )
    facility_costs: float = Field(
        0.0, description="Total fixed costs for opening the facilities"
    )
    transport_costs: float = Field(
        0.0, description="Total transportation costs for serving the customers"
    )
    total_costs: float = Field(
        0.0, description="Total costs"
    )

    @model_validator(mode="after")
    def validate_total_costs(self) -> 'Solution':
        expected_total = self.facility_costs + self.transport_costs
        if not abs(self.total_costs - expected_total) < 1e-6:
            raise ValueError(
                f"Total costs ({self.total_costs}) must equal facility + transport costs ({expected_total})"
            )
        return self

    def save(self, output_folder: Path) -> None:
        """
        Saves the solution to a JSON file.

        Args:
            output_folder: Path to the folder where the JSON file will be saved.
        """
        file_path = output_folder / 'solution.json'
        with open(file_path, 'w') as f:
            f.write(self.model_dump_json(indent=4))
            print(f"Solution saved to {file_path}")
