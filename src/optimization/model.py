from pathlib import Path

import pulp
from pulp import LpProblem

from business.facility_location import FacilityLocation
from business.solution import Solution
from optimization.constraints import assign_customers, assigned_customers_imply_open_facility
from optimization.variables import set_variables
from optimization.objective_function import set_objective


class OptimizationModelPulp:
    """
    Represents an uncapacitated facility location problem.
    """

    def __init__(self, instance: FacilityLocation) -> None:
        self.instance = instance

        # Initialize the optimization model
        self.model = LpProblem("UFLP", pulp.LpMinimize)

        # Set all the variables
        set_variables(self.model, self.instance)

        # Set all the constraints
        assign_customers(self.model, self.instance)
        assigned_customers_imply_open_facility(self.model, self.instance)

        # BUG 3: integration test bug: comment the assigned_customers_imply_open_facility function. This will
        # cause the unit tests to pass, but the integration tests to fail, as the formulation is not assembled correctly.

        # Set the objective function
        set_objective(self.model, self.instance)

    def solve(self) -> Solution:
        # This is CBC Solver
        self.model.solve(pulp.PULP_CBC_CMD(msg=True))
        objective_function_value = pulp.value(self.model.objective)
        print("Status:", pulp.LpStatus[self.model.status])
        print("Objective Function Value:", objective_function_value)

        # Assemble the solution now
        binary_threshold = 0.9
        open_facilities = [
            f for f in range(self.instance.num_facilities)
            if pulp.value(self.model.y[f]) > binary_threshold
        ]
        customer_assignment = [
            next(
                f for f in range(self.instance.num_facilities)
                if pulp.value(self.model.x[(f, c)]) > binary_threshold
            )
            for c in range(self.instance.num_customers)
        ]
        objective_facility_costs = pulp.value(self.model.objective_facility_costs)
        objective_transport_costs = pulp.value(self.model.objective_transport_costs)
        print("\tFacility Costs in Objective:", objective_facility_costs)
        print("\tTransport Costs in Objective:", objective_transport_costs)

        return Solution(
            open_facilities=open_facilities,
            customer_assignment=customer_assignment,
            facility_costs=objective_facility_costs,
            transport_costs=objective_transport_costs,
            total_costs=objective_function_value,
        )

    def save_model(self, folder_path: Path) -> None:
        model_path = folder_path / "model.mps"
        self.model.writeMPS(str(model_path))
        print(f"Model saved to {model_path}")