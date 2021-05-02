import argparse
from typing import List, Union
import utils


def evaluate(expression: str, at: Union[float, List[float]]) -> List[float]:
    evaluator = utils.Evaluator(expression, at)
    return evaluator.results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expression', type=str, required=True, help='expression to be evaluated for given values')
    parser.add_argument('--at', type=str, required=True, help='list of values to be evaluated in expression')
    args = parser.parse_args()
    expression = args.expression
    at = [float(v) for v in args.at.split(',')]
    result = evaluate(expression, at)
    print(f'evaluating expression {expression} for values {at}.')
    print(f'result: {result}')


if __name__ == '__main__':
    main()
