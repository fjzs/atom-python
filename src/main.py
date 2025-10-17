from business.instance_builder import create_random_instance
from services.case_solver import CaseSolver
from drawing.draw import plot_scenario
import argparse
from datetime import datetime
from pathlib import Path

ROOT_FOLDER = Path(__file__).parent.parent.resolve()
INPUT_FOLDER = ROOT_FOLDER / "input"
OUTPUT_FOLDER = ROOT_FOLDER / "output"


def solve_case(case_name) -> None:
    """
    Solve a given case from the input folder.
    """

    # This is the timestamp for this run, it will be used to create the output folder individual run
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = str(Path(OUTPUT_FOLDER) / case_name / timestamp)
    input_path = str(Path(INPUT_FOLDER) / case_name)

    # Now run the solver
    solver = CaseSolver(input_folder=input_path, output_folder=output_path)
    solver.run()


def build_instance(num_facilities, num_customers):
    print(
        f"\n============== Building new random instance with {num_facilities} facilities and {num_customers} customers =============="
    )
    # Create the input folder if not exists
    input_path = Path(INPUT_FOLDER)
    input_path.mkdir(parents=True, exist_ok=True)

    # Name the new folder case as the next case recycling the indices
    prefix = "case"
    existing_numbers = set()
    for f in input_path.iterdir():
        if f.is_dir() and f.name.startswith(prefix):
            num_str = f.name[len(prefix) :]
            if num_str.isdigit():
                existing_numbers.add(int(num_str))
    # Find the smallest missing number starting from 1
    next_index = 1
    while next_index in existing_numbers:
        next_index += 1
    # Build the folder case path
    case_folder = input_path / f"{prefix}{next_index}"
    case_folder.mkdir(parents=True, exist_ok=True)

    # Create the new instance
    instance = create_random_instance(num_facilities, num_customers)

    # Save this instance in the case folder
    instance.save_to_json(folder_path=case_folder, filename="data.json")

    # Draw the map and save it into the folder as well
    plot_scenario(instance, folder_path=case_folder)

    print(f"Instance saved to {case_folder}")


def main():
    parser = argparse.ArgumentParser(description="Optimization program CLI")
    # "dest" is the attribute name where the subcommand will be stored, eg: solve or build
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # Subcommand: solve
    parser_solve = subparsers.add_parser("solve", help="Solve a given instance")
    parser_solve.add_argument(
        "case",
        nargs="?",
        default="case1",
        type=str,
        help="Name of the instance to solve in the input folder",
    )

    # Subcommand: build
    parser_build = subparsers.add_parser(
        "build", help="Build a random new instance on a 100 x 100 grid"
    )
    parser_build.add_argument(
        "--f", "-f", default=3, type=int, help="Number of facilities"
    )
    parser_build.add_argument(
        "--c", "-c", default=10, type=int, help="Number of customers"
    )

    # Parse arguments
    args = parser.parse_args()

    # Dispatch based on subcommand
    if args.command == "solve":
        solve_case(args.case)
    elif args.command == "build":
        build_instance(args.f, args.c)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

    # For debugging:
    # solve_case("case3")
