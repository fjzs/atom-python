import pulp
from pulp import LpAffineExpression, LpConstraint


def compare(expected_vars: dict[str, pulp.LpVariable],
            expected_model: pulp.LpProblem,
            actual_vars: dict[str, pulp.LpVariable],
            actual_model: pulp.LpProblem) -> bool:
    """
    Compares two optimization models formulations for equality.

    Args:
        expected_vars (dict[str, pulp.LpVariable]): Variables of the first model
        expected_model (pulp.LpProblem): The first optimization model
        actual_vars (dict[str, pulp.LpVariable]): Variables of the second model
        actual_model (pulp.LpProblem): The second optimization model

    Returns:
        bool: True if the models are equal, False otherwise
    """

    print("\nComparing expected model with actual model...")

    # Compare variables:
    if expected_vars != actual_vars:
        print("x Variables differ")
        return False
    print("✓ Variables match")

    # Compare constraints
    if not constraints_keys_are_equal(expected_model.constraints, actual_model.constraints):
        print("x Constraints keys differ")
        return False
    print("✓ Constraints keys match")

    # Compare the constraints expressions:
    for name, con1 in expected_model.constraints.items():
        con2 = actual_model.constraints[name]
        if not are_constraints_equal(con1, con2):
            print(f"x Constraint '{name}' differs")
            return False
    print("✓ Constraints expressions match")

    # Compare objective function sense
    if expected_model.sense != actual_model.sense:
        print("x Objective senses differ: expected " + str(expected_model.sense) + ", actual " + str(actual_model.sense))
        return False
    print("✓ Objective senses match")

    # Compare the objective function expressions
    if not are_expressions_equal(expected_model.objective, actual_model.objective):
        print("x Objective functions differ")
        return False
    print("✓ Objective functions match")

    return True


def are_expressions_equal(expected: LpAffineExpression, actual: LpAffineExpression) -> bool:
    """
    Compares two linear expressions for equality.
    """
    if len(expected.items()) != len(actual.items()):
        print("Number of terms in expressions differ, expected "+ str(len(expected.items())) + ", actual " + str(len(actual.items())))
        return False
    if expected.constant != actual.constant:
        print("Constants in expressions differ, expected " + str(expected.constant) + ", actual " + str(actual.constant))
        return False
    for (var1, coeff1), (var2, coeff2) in zip(expected.items(), actual.items()):
        if var1.name != var2.name:
            print("Variables in expressions differ, expected " + var1.name + ", actual " + var2.name)
            return False
        if coeff1 != coeff2:
            print("Coefficients for variable " + var1.name + " in expressions differ, expected " + str(coeff1) + ", actual " + str(coeff2))
            return False
    return True


def are_constraints_equal(constraint1: LpConstraint, constraint2: LpConstraint) -> bool:
    if constraint1.sense != constraint2.sense:
        print("Constraint senses differ, expected " + str(constraint1.sense) + ", actual " + str(constraint2.sense))
        return False
    if constraint1.constant != constraint2.constant:
        print("Constraint constants differ, expected " + str(constraint1.constant) + ", actual " + str(constraint2.constant))
        return False
    return are_expressions_equal(constraint1.expr, constraint2.expr)


def constraints_keys_are_equal(constraints_expected: dict[str, LpConstraint],
                               constraints_actual: dict[str, LpConstraint]) -> bool:
    """
    Checks if the keys of two constraints dictionaries are equal.
    :param constraints_expected:
    :param constraints_actual:
    :return:
    """
    # Get the keys first
    keys_expected = constraints_expected.keys()
    keys_actual = constraints_actual.keys()

    # Elements in expected, but not in actual
    in_expected_not_actual = keys_expected - keys_actual
    if in_expected_not_actual:
        print("Constraints in expected, but not in actual:")
        for key in in_expected_not_actual:
            print(f"\t{key}")
        return False

    # Elements in actual, but not in expected
    in_actual_not_expected = keys_actual - keys_expected
    if in_actual_not_expected:
        print("Constraints in actual, but not in expected:")
        for key in in_actual_not_expected:
            print(f"\t{key}")
        return False

    return True
