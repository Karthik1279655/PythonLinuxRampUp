import argparse
import pytest
import logging


class Calculator:
    def __init__(self, number1, number2, operation):
        self.number1 = number1
        self.number2 = number2
        self.operation = operation

    def calculate(self):
        n1 = int(self.number1)
        n2 = int(self.number2)
        result = None

        if self.operation == "add":
            result = n1 + n2
        elif self.operation == "subtract":
            result = n1 - n2
        elif self.operation == "multiply":
            result = n1 * n2
        else:
            print("Unsupported Operation")

        return result


def run_tests(calculator, operation, number1, number2, expected_result):
    calculator.number1 = number1
    calculator.number2 = number2
    calculator.operation = operation

    result = calculator.calculate()

    assert result == expected_result


def main():
    parser = argparse.ArgumentParser(description="A simple calculator program")
    parser.add_argument("--number1", help="The first number", required=True)
    parser.add_argument("--number2", help="The second number", required=True)
    parser.add_argument("--operation", help="The operation to perform", choices=["add", "subtract", "multiply"],
                        required=True)
    args = parser.parse_args()

    calculator = Calculator(args.number1, args.number2, args.operation)

    try:
        run_tests(calculator, args.operation, args.number1, args.number2, eval(input("Enter expected result: ")))
    except AssertionError:
        logging.error("Tests failed")
        return 1

    logging.info("Tests passed")
    return 0


@pytest.mark.parametrize("number1, number2, operation, expected_result", [
    ("2", "3", "add", 5),
    ("5", "3", "subtract", 2),
    ("2", "3", "multiply", 6),
])
def test_calculate(number1, number2, operation, expected_result):
    calculator = Calculator(number1, number2, operation)
    run_tests(calculator, operation, number1, number2, expected_result)
