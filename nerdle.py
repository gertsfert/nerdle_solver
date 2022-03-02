from pathlib import Path
from typing import List, Tuple


DIGITS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
OPERATIONS = ["+", "-", "/", "*"]


def operate_on_numbers(num1, op, num2) -> float:
    if op == "+":
        return num1 + num2
    if op == "-":
        return num1 - num2
    if op == "*":
        return num1 * num2
    if op == "/":
        return num1 / num2


def parse_nums_and_ops(lhs: List[str]) -> Tuple[List[int], List[str]]:
    nums = []
    ops = []

    parsed_num = ""
    for char in lhs:
        if char in DIGITS:
            parsed_num += char
        else:
            nums.append(int(parsed_num))
            ops.append(char)
            parsed_num = ""

    nums.append(int(parsed_num))

    return nums, ops


def calculate_lhs(lhs: List[str]) -> float:
    nums, ops = parse_nums_and_ops(lhs)
    # good example to test with 4 + 2 * 6 / 3

    # do priority ops first
    prio_ops = [(i, op) for i, op, in enumerate(ops) if op in ["*", "/"]]

    prio_offset = 0
    for prio_i_op in prio_ops:
        prio_i, prio_op = prio_i_op

        prio_i -= prio_offset
        result = operate_on_numbers(
            num1=nums[prio_i], op=prio_op, num2=nums[prio_i + 1]
        )

        # have result - edit arrays with result
        # remove operated numbers
        nums = nums[:prio_i] + [result] + nums[prio_i + 2 :]

        # remove op
        ops.pop(prio_i)

        # reduce index numbers of the rest of prio_ops to compensate
        prio_offset += 1

    # can now just do left to right
    result = nums[0]
    for i, op in enumerate(ops):
        result = operate_on_numbers(result, op, nums[i + 1])

    return result


def is_valid_solution(solution: List[str]) -> bool:
    equals_pos = solution.index("=")
    rhs = int("".join(solution[equals_pos + 1 :]))
    lhs = calculate_lhs(solution[:equals_pos])

    return abs(rhs - lhs) < 0.0001


def format_solution(solution: List[str]) -> str:
    s = solution[0]

    prev = solution[0]
    for c in solution[1:]:
        if prev in DIGITS and c in DIGITS:
            s += c
        else:
            s += f" {c}"

        prev = c

    return s


def get_options(num_chars, solution: List[str]) -> List[str]:

    has_eq = "=" in solution
    index = len(solution)

    if len(solution) == 0:
        return DIGITS

    prev_c = solution[-1]

    is_forced_equals = not has_eq and index == num_chars - 2

    # is next character forced to be equals?
    next_is_forced_equals = not has_eq and index + 1 == num_chars - 2

    is_forced_digit = (
        (index == num_chars - 1)
        or prev_c in OPERATIONS
        or has_eq
        or next_is_forced_equals
    )

    can_be_equals = not has_eq and not prev_c in OPERATIONS

    if is_forced_equals:
        return ["="]

    if is_forced_digit:
        return DIGITS

    if can_be_equals:
        return DIGITS + OPERATIONS + ["="]

    return DIGITS + OPERATIONS


def generate_solutions(
    num_chars, solution: List[str] = [], solutions: List[List[str]] = []
):
    """Generates a list of all syntactically correct solutions given
    starting characters"""

    # solution is full length, it is the only option
    if len(solution) >= num_chars:
        solutions.append(solution)

    # otherwise return list of possible solutions
    else:
        for option in get_options(num_chars, solution):
            generate_solutions(num_chars, solution + [option], solutions)

    return solutions


def find_all_solutions():
    all_solutions = generate_solutions(num_chars=6)
    valid_solutions = [
        solution for solution in all_solutions if is_valid_solution(solution)
    ]

    print("done")
    print(f"{len(valid_solutions)} valid solutions found")

    return valid_solutions


if __name__ == "__main__":
    solutions = find_all_solutions()

    solution_strs = [format_solution(s) for s in solutions]

    outpath = Path("generated_solutions", "nerdle_solutions.txt")
    with open(outpath, "w") as file:
        file.write("\n".join(solution_strs))

    print(f"saved to {outpath}")
