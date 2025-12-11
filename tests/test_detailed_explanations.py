import json
import sys
sys.path.insert(0, '/Users/simsek/dev/Group_Project')

from src.app.core.step_solver.operation_router import OperationRouter

def print_step_details(step, step_num):
    print(f"\n{'='*80}")
    print(f"STEP {step_num}: {step.get('title', 'Unknown').upper()}")
    print(f"{'='*80}")
    print(f"Expression: {step.get('expression', '')}")
    print(f"Rule: {step.get('rule', '')}")

    pack = step.get('explanation_pack', {})

    print(f"\n📖 EXPLANATION:")
    print(f"   {step.get('explanation', '')}")

    if pack.get('hint'):
        print(f"\n{pack['hint']}")

    if pack.get('common_mistake'):
        print(f"\n{pack['common_mistake']}")

    if pack.get('follow_up'):
        print(f"\n{pack['follow_up']}")

def test_operation(operation, expression, optional_input="", description=""):
    print(f"\n\n{'#'*80}")
    print(f"# TEST: {description}")
    print(f"# Operation: {operation}")
    print(f"# Expression: {expression}")
    if optional_input:
        print(f"# Optional Input: {optional_input}")
    print(f"{'#'*80}")

    router = OperationRouter(use_enhanced_explanations=True)
    result = router.generate_steps(operation, expression, optional_input)

    if result.get('success'):
        steps = result.get('steps', [])
        for i, step in enumerate(steps, 1):
            print_step_details(step, i)

        if result.get('solution'):
            print(f"\nFINAL SOLUTION: {result['solution']}")
    else:
        print(f"\n ERROR: {result.get('error', 'Unknown error')}")

    print("\n")

def main():

    print("\n" + "="*80)
    print("DETAILED EXPLANATIONS TEST SUITE")
    print("="*80)

    test_operation(
        "calculate",
        "5 + 3 * 2",
        description="Simple arithmetic with order of operations"
    )

    test_operation(
        "simplify",
        "2*x + 3*x + 5",
        description="Combining like terms"
    )

    
    test_operation(
        "expand",
        "(x + 2)*(x + 3)",
        description="Expanding binomial product"
    )

    
    test_operation(
        "factor",
        "x**2 + 5*x + 6",
        description="Factoring quadratic expression"
    )

    
    test_operation(
        "solve",
        "2*x + 5 = 13",
        description="Solving linear equation"
    )

    
    test_operation(
        "differentiate",
        "x**2 + 3*x + 1",
        optional_input="x",
        description="Finding derivative"
    )

    
    test_operation(
        "simplify",
        "3*x + 2*y - x + 4*y",
        description="Simplifying with multiple variables"
    )

    
    test_operation(
        "calculate",
        "20 / 4 + 3",
        description="Division with addition"
    )

    print("\n" + "="*80)
    print("TEST SUITE COMPLETE!")
    print("="*80)
    print("\n Try these expressions in the calculator app:")
    print("   1. Simplify: 5*x - 2*x + 7")
    print("   2. Expand: (x - 1)*(x + 4)")
    print("   3. Factor: x**2 - 9")
    print("   4. Solve: 3*x - 7 = 11")
    print("   5. Calculate: 2 + 3 * 4 - 1")
    print("\n")

if __name__ == "__main__":
    main()
