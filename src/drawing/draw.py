import matplotlib
matplotlib.use('Agg') # use this non-interactive backend if you are running this on a headless environment
import matplotlib.pyplot as plt
from pathlib import Path
from business.facility_location import FacilityLocation
from business.instance_builder import GRID_SIZE
from business.solution import Solution


def plot_scenario(instance: FacilityLocation, folder_path: Path) -> None:
    """
    Plot a facility location instance on a 2D grid and save it as PNG.

    Args:
        instance: FacilityLocation instance to plot.
        folder_path: Path to the folder where the PNG will be saved.

    Returns:
        str: Path to the saved PNG file.
    """
    # Prepare output path
    filename = "map.png"
    file_path = folder_path / filename

    # Unpack coordinates
    fx, fy = zip(*instance.facilities_location)
    cx, cy = zip(*instance.customers_location)

    # Plot
    plt.figure(figsize=(8, 8))

    # Hollow squares for facilities, we don't know yet what is the solution
    plt.scatter(
        fx, fy, s=150, edgecolor="red", facecolors="none", marker="s", linewidth=1.5
    )

    # Filled circles for customers
    plt.scatter(cx, cy, s=50, c="blue", marker="o")

    plt.xlim(0, GRID_SIZE)
    plt.ylim(0, GRID_SIZE)
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.title(
        f"Facility Location: {instance.num_facilities} facilities, {instance.num_customers} customers"
    )
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_solution(
    instance: FacilityLocation, solution: Solution, folder_path: Path
) -> None:
    """
    Plot a facility location solution on a 2D grid and save it as PNG.

    Args:
        instance: FacilityLocation instance with coordinates.
        solution: Solution object containing open facilities and customer assignments.
        folder_path: Folder where the PNG will be saved.
    """
    file_path = folder_path / "solution.png"

    # Unpack coordinates
    fx, fy = zip(*instance.facilities_location)
    cx, cy = zip(*instance.customers_location)

    plt.figure(figsize=(8, 8))

    # Hollow squares for unused facilities
    unused_facilities = [
        f for f in range(instance.num_facilities) if f not in solution.open_facilities
    ]
    if unused_facilities:
        plt.scatter(
            [fx[f] for f in unused_facilities],
            [fy[f] for f in unused_facilities],
            s=150,
            edgecolor="red",
            facecolors="none",
            marker="s",
            linewidth=1.5,
            label="Facility (closed)",
        )

    # Filled squares for open facilities
    if solution.open_facilities:
        plt.scatter(
            [fx[f] for f in solution.open_facilities],
            [fy[f] for f in solution.open_facilities],
            s=150,
            c="red",
            marker="s",
            linewidth=1.5,
            label="Facility (opened)",
        )

    # Customers
    plt.scatter(cx, cy, s=50, c="blue", marker="o", label="Customers")

    # Draw lines from each customer to its assigned facility
    for c_idx, f_idx in enumerate(solution.customer_assignment):
        plt.plot(
            [cx[c_idx], fx[f_idx]],
            [cy[c_idx], fy[f_idx]],
            c="black",
            linestyle="--",
            linewidth=0.8,
        )

    plt.xlim(0, GRID_SIZE)
    plt.ylim(0, GRID_SIZE)
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.title(
        f"Facility Location Solution: {len(solution.open_facilities)} facilities opened"
    )
    plt.grid(True, linestyle="--", alpha=0.6)

    # Legend outside
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))

    plt.tight_layout()
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Solution plot saved to {file_path}")
