# ATOM
ATOM stands for Automated Testing for Optimization Models. This is a framework to test optimization models with continuous integration techniques.
- Patent Pending
- © 2025 American Airlines.

## Installation
(1) Create a virtual environment with Python 3.13:

`python -m venv .venv`

(2) Activate the virtual environment (on Windows)

`.\.venv\Scripts\Activate.ps1`

(3) Install the requirements

`pip install -r requirements.txt`

## Example with the Uncapacitated Facility Location Problem
The Uncapacitated Facility Location Problem (UFLP) is a classic optimization problem where the 
goal is to determine the optimal locations for facilities to minimize costs while meeting customer demand. 
In this example, we will demonstrate how to implement ATOM on this problem.

### The optimization model
Sets:
- $F$: Set of potential facility locations.
- $C$: Set of customers.

Parameters:
- $h_f$: fixed cost of opening facility $f$.
- $d_{fc}$: cost of serving customer $c$ from facility $f$.

Variables:
- $y_f$: binary variable indicating 1 if facility $f$ is opened, 0 otherwise.
- $x_{fc}$: binary variable indicating 1 if customer $c$ is served by facility $f$, 0 otherwise.

Constraints:
- Each customer is served by exactly one facility:

   $$\sum_{f \in F} x_{fc} = 1 \quad \forall c \in C$$
- A customer can only be served by an open facility:

   $$x_{fc} \leq y_f \quad \forall f \in F, c \in C$$

Objetive function:
- Minimize the total cost of opening facilities and serving customers:

   $$\text{Minimize} \quad \sum_{f \in F} h_f y_f + \sum_{f \in F} \sum_{c \in C} d_{fc} x_{fc}$$


### Create a case
To create a case use this command through the terminal from the root folder of the project:

`python src/main.py build -f 3 -c 10`
- This will create a case with 3 facilities and 10 customers randomly set in a grid of 100x100.
- The folder will be saved in the `input` folder at the root of the project.

### Solve a case
To solve a case use this command through the terminal from the root folder of the project:

`python src/main.py solve case_name`
- Replace `case_name` with the name of the folder created previously, example:
`python src/main.py solve case1`
- The solution will be saved in the `output` folder at the root of the project.

## Running the tests
To run all the test use this command through the terminal from the root folder of the project:

`pytest`

To run only unit tests:

`pytest tests/unit`

To run only integration tests:

`pytest tests/integration`

## Example of detecting bugs:
- Look in the code for "BUG 1" to see an example of a bug being caught by unit tests (variable not created correctly)
- Look in the code for "BUG 2" to see an example of a bug being caught by unit tests (constraint not created correctly)
- Look in the code for "BUG 3" to see an example of a bug being caught by integration tests (wrong objective function)
