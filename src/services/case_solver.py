from pathlib import Path
from business.instance_loader import load_from_json
from drawing.draw import plot_solution, plot_scenario
from optimization.model import OptimizationModelPulp


class CaseSolver:
    """
    Runs the optimization solver for a given Facility Location case.
    """

    def __init__(self, input_folder: str, output_folder: str):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.instance = None
        self._load_instance()

    def _load_instance(self):
        data_path = Path(self.input_folder) / "data.json"
        if not data_path.exists():
            raise FileNotFoundError(
                f"Case '{self.input_folder}' does not contain a data.json file."
            )
        else:
            self.instance = load_from_json(data_path)
            print("Instance loaded successfully")

    def run(self):
        print("\n======= Solving case =======")
        # ----- Phase 1: LOADING DATA -----
        self._load_instance()
        # set the output folder
        output_path = Path(self.output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        # Save the input data to the output folder for reference
        self.instance.save_to_json(output_path)
        plot_scenario(self.instance, output_path)

        # ----- Phase 2: OPTIMIZATION -----
        # Part 1: build the concrete optimization
        model = OptimizationModelPulp(self.instance)

        # Part 2: save the model to a file
        model.save_model(folder_path=output_path)
        
        # Part 3: solve the optimization and get the solution
        solution = model.solve()

        # ----- Phase 3: POST-PROCESSING -----
        solution.save(output_path)
        plot_solution(self.instance, solution, output_path)
        return solution
