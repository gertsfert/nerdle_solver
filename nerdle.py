from typing import List, Tuple
from tqdm import tqdm

DIGITS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
OPERATIONS = ["+", "-", "/", "*"]

CHARS = 8
MAX_DIGITS_FOR_ANSWER = 5


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
    s = ""

    prev = ""
    for c in solution:
        if prev in DIGITS and c in DIGITS:
            s += c
        else:
            s += f" {c}"

        prev = c

    return s


def get_options(solution: List[str]) -> List[str]:

    has_eq = "=" in solution
    index = len(solution)

    if len(solution) == 0:
        return DIGITS

    prev_c = solution[-1]

    is_forced_equals = not has_eq and index == CHARS - 2

    # is next character forced to be equals?
    next_is_forced_equals = not has_eq and index + 1 == CHARS - 2

    is_forced_digit = (
        (index == CHARS - 1) or prev_c in OPERATIONS or has_eq or next_is_forced_equals
    )

    can_be_equals = not has_eq and not prev_c in OPERATIONS

    if is_forced_equals:
        return ["="]

    if is_forced_digit:
        return DIGITS

    if can_be_equals:
        return DIGITS + OPERATIONS + ["="]

    return DIGITS + OPERATIONS


def find_all_solutions():
    all_solutions = []
    valid_solutions = []

    solution = []

    for c0 in tqdm(get_options(solution), desc="c0", position=0, leave=False):
        solution.append(c0)
        for c1 in tqdm(get_options(solution), desc="c1", position=1, leave=False):
            solution.append(c1)
            for c2 in tqdm(get_options(solution), desc="c2", position=2, leave=False):
                solution.append(c2)
                for c3 in get_options(solution):
                    solution.append(c3)
                    for c4 in get_options(solution):
                        solution.append(c4)
                        for c5 in get_options(solution):
                            solution.append(c5)
                            for c6 in get_options(solution):
                                solution.append(c6)
                                for c7 in get_options(solution):
                                    solution.append(c7)

                                    all_solutions.append(solution)
                                    if is_valid_solution(solution):
                                        valid_solutions.append(solution)

                                    solution = solution[:7]
                                solution = solution[:6]
                            solution = solution[:5]
                        solution = solution[:4]
                    solution = solution[:3]
                solution = solution[:2]
            solution = solution[:1]
        solution = []

    print("done")
    print(f"{len(valid_solutions)} valid solutions found")

    return valid_solutions


if __name__ == "__main__":
    solutions = find_all_solutions()

    solution_strs = [format_solution(s) for s in solutions]

    outpath = "nerdle_solutions.txt"
    with open(outpath, "w") as file:
        file.write("\n".join(solution_strs))

    print(f"saved to {outpath}")
