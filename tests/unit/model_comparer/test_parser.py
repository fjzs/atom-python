from pulp import LpVariable, LpProblem, LpConstraint, LpConstraintEQ, LpAffineExpression, LpConstraintLE, LpMinimize

from model_comparer.parser import parse_model_file
from pathlib import Path

SCENARIOS_FOLDER = Path(__file__).parent

#---------------------------------------------------------------------------------------------------------------------#
# Note: this file tests the parser works correctly. It does so by checking that the parsed model.mps file saved on this
# folder is correctly read.
#---------------------------------------------------------------------------------------------------------------------#

def __are_expressions_equal(expr1: LpAffineExpression, expr2: LpAffineExpression) -> bool:
    if len(expr1.items()) != len(expr2.items()):
        return False
    if expr1.constant != expr2.constant:
        return False
    for (var1, coeff1), (var2, coeff2) in zip(expr1.items(), expr2.items()):
        if var1.name != var2.name or coeff1 != coeff2:
            return False
    return True

def __are_constraints_equal(constraint1: LpConstraint, constraint2: LpConstraint) -> bool:
    if constraint1.sense != constraint2.sense:
        return False
    if constraint1.constant != constraint2.constant:
        return False
    return __are_expressions_equal(constraint1.expr, constraint2.expr)

def test_2facilities_2customers_instance():
    # ARRANGE
    filepath = str(SCENARIOS_FOLDER / "model.mps")

    # Expected variables
    expected_variables: dict[str, LpVariable] = dict()
    expected_variables['assign_facility_to_customer_(0,_0)'] = LpVariable('assign_facility_to_customer_(0,_0)', lowBound=0, upBound=1, cat='Integer')
    expected_variables['assign_facility_to_customer_(0,_1)'] = LpVariable('assign_facility_to_customer_(0,_1)', lowBound=0, upBound=1, cat='Integer')
    expected_variables['assign_facility_to_customer_(1,_0)'] = LpVariable('assign_facility_to_customer_(1,_0)', lowBound=0, upBound=1, cat='Integer')
    expected_variables['assign_facility_to_customer_(1,_1)'] = LpVariable('assign_facility_to_customer_(1,_1)', lowBound=0, upBound=1, cat='Integer')
    expected_variables['open_facility_0'] = LpVariable('open_facility_0', lowBound=0, upBound=1, cat='Integer')
    expected_variables['open_facility_1'] = LpVariable('open_facility_1', lowBound=0, upBound=1, cat='Integer')

    # Expected objective
    expected_objective = LpAffineExpression()
    expected_objective += 49.7 * expected_variables['assign_facility_to_customer_(0,_0)']
    expected_objective += 18.2 * expected_variables['assign_facility_to_customer_(0,_1)']
    expected_objective += 92.8 * expected_variables['assign_facility_to_customer_(1,_0)']
    expected_objective += 51.0 * expected_variables['assign_facility_to_customer_(1,_1)']
    expected_objective += 50.0 * expected_variables['open_facility_0']
    expected_objective += 50.0 * expected_variables['open_facility_1']

    # Expected constraints
    expected_constraints: dict[str, LpConstraint] = dict()
    expected_constraints['AssignCustomer_0'] = LpConstraint(
        e=expected_variables['assign_facility_to_customer_(0,_0)'] + expected_variables['assign_facility_to_customer_(1,_0)'],
        sense=LpConstraintEQ,
        rhs=1,
        name='AssignCustomer_0'
    )
    expected_constraints['AssignCustomer_1'] = LpConstraint(
        e=expected_variables['assign_facility_to_customer_(0,_1)'] + expected_variables['assign_facility_to_customer_(1,_1)'],
        sense=LpConstraintEQ,
        rhs=1,
        name='AssignCustomer_1'
    )
    expected_constraints['OpenFacility_0_for_Customer_0'] = LpConstraint(
        e=expected_variables['assign_facility_to_customer_(0,_0)'] - expected_variables['open_facility_0'],
        sense=LpConstraintLE,
        rhs=0,
        name='OpenFacility_0_for_Customer_0'
    )
    expected_constraints['OpenFacility_0_for_Customer_1'] = LpConstraint(
        e=expected_variables['assign_facility_to_customer_(0,_1)'] - expected_variables['open_facility_0'],
        sense=LpConstraintLE,
        rhs=0,
        name='OpenFacility_0_for_Customer_1'
    )
    expected_constraints['OpenFacility_1_for_Customer_0'] = LpConstraint(
        e=expected_variables['assign_facility_to_customer_(1,_0)'] - expected_variables['open_facility_1'],
        sense=LpConstraintLE,
        rhs=0,
        name='OpenFacility_1_for_Customer_0'
    )
    expected_constraints['OpenFacility_1_for_Customer_1'] = LpConstraint(
        e=expected_variables['assign_facility_to_customer_(1,_1)'] - expected_variables['open_facility_1'],
        sense=LpConstraintLE,
        rhs=0,
        name='OpenFacility_1_for_Customer_1'
    )

    # ACT
    actual_variables, actual_model = parse_model_file(filepath)

    # ASSERT
    # Check the variables
    assert expected_variables == actual_variables

    # Check the constraints
    assert len(expected_constraints) == len(actual_model.constraints)
    for name, expected_constraint in expected_constraints.items():
        actual_constraint = actual_model.constraints[name]
        assert __are_constraints_equal(expected_constraint, actual_constraint)

    # Check the objective expression
    assert __are_expressions_equal(expected_objective, actual_model.objective)

    # Check the objective sense
    assert actual_model.sense == LpMinimize