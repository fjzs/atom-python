from pathlib import Path
from business.facility_location import FacilityLocation


def load_from_json(file_path: Path) -> FacilityLocation:
    """
    Load a FacilityLocation instance from a JSON file.

    Args:
        file_path: Path to the JSON file.

    Returns:
        FacilityLocation instance.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()

    # Use Pydantic's model_validate_json
    return FacilityLocation.model_validate_json(data)
