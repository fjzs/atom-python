from pulp import LpProblem, LpVariable
from pathlib import Path


def parse_model_file(filepath: str) -> tuple[dict[str, LpVariable], LpProblem]:
    """
    Parses an optimization model file

    Args:
        filepath (str): Path to the model file

    Returns:
        dict[str, LpVariable]: A dictionary of variables in the model
        LpProblem: The parsed optimization model
    """

    # Check if the file exists
    if not Path(filepath).is_file():
        raise FileNotFoundError(f"File not found: {filepath} from {Path.cwd()}")

    # Parse the model file
    # Note: we picked .mps files because pulp supports natively the reading of this format, but you can pick
    # whatever format you want. More info here: https://coin-or.github.io/pulp/guides/how_to_export_models.html
    if not filepath.endswith(".mps"):
        raise ValueError(f"Unsupported file format: {filepath}. Only .mps files are supported.")

    return LpProblem.fromMPS(filepath)
