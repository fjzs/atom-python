import pytest
from pathlib import Path
from datetime import datetime

from model_comparer.comparator import compare
from model_comparer.parser import parse_model_file
from services.case_solver import CaseSolver

# Path relative to this test file
INTEGRATION_TEST_CASES = (
    Path(__file__).parent.parent / "integration" / "scenarios"
)
SCENARIOS = [f.name for f in INTEGRATION_TEST_CASES.iterdir() if f.is_dir()]
OUTPUT_FOLDER = Path(__file__).parent.parent.parent / "output" / "integration"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

@pytest.mark.parametrize("case_name", SCENARIOS)
def test_solver_integration(case_name):
    """
    Runs a case end-to-end and saves the output in a specific folder so we can check some conditions on the output
    """
    # Define the output folder to store the results of this case
    print(f"\nRunning integration scenario: {case_name}")
    output_run_folder = str(OUTPUT_FOLDER / TIMESTAMP / case_name)
    case_input_folder = str(INTEGRATION_TEST_CASES / case_name)

    # Run the solver
    solver = CaseSolver(case_input_folder, output_run_folder)
    solver.run()

    # Integration tests checks:
    # Check: the formulation must be the same
    expected_model_file = Path(case_input_folder) / "model.mps"
    actual_model_file = Path(output_run_folder) / "model.mps"
    expected_variables, expected_model = parse_model_file(str(expected_model_file))
    actual_variables, actual_model = parse_model_file(str(actual_model_file))

    # Run the comparison
    assert compare(expected_variables, expected_model, actual_variables, actual_model)