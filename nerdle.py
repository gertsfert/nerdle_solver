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


class Solution:
    def __init__(self, num_chars, chars: List[str] = None):
        self.num_chars = num_chars

        if chars is None:
            self.chars = []
        else:
            self.chars = chars

    @property
    def has_equals(self):
        return "=" in self.chars

    @property
    def is_full(self):
        return len(self.chars) >= self.num_chars

    @property
    def equals_index(self):
        try:
            return self.chars.index("=")
        except IndexError:
            return None

    def add_char(self, char):
        self.chars.append(char)

    @property
    def is_valid_solution(self) -> bool:
        if len(self.chars) < self.num_chars:
            return False

        return abs(self.rhs_value - self.lhs_value) < 0.0001

    @property
    def lhs(self) -> List[str]:
        return self.chars[: self.equals_index]

    @property
    def lhs_value(self):
        nums, ops = self.parse_lhs_nums_and_ops()

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

    @property
    def rhs_value(self):
        return int("".join(self.chars[self.equals_index + 1 :]))

    @property
    def rhs(self) -> List[str]:
        return self.chars[self.equals_index + 1 :]

    def __str__(self) -> str:
        s = self.chars[0]
        prev = self.chars[0]

        for c in self.chars[1:]:
            if prev in DIGITS and c in DIGITS:
                s += c
            else:
                s += f" {c}"

            prev = c

        return s

    def parse_lhs_nums_and_ops(self) -> Tuple[List[int], List[str]]:
        nums = []
        ops = []

        lhs = self.chars[: self.equals_index]

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

    def get_options_for_next_char(self) -> List[str]:
        index = len(self.chars)

        if index == 0:
            return DIGITS

        last_char = self.chars[-1]

        # need two characters for 'equals number'
        is_forced_equals = not self.has_equals and index == self.num_chars - 2

        # is next character forced to be equals?
        next_is_forced_equals = not self.has_equals and index + 1 == self.num_chars - 2

        is_forced_digit = (
            (index == self.num_chars - 1)
            or last_char in OPERATIONS
            or self.has_equals
            or next_is_forced_equals
        )

        can_be_equals = not self.has_equals and not last_char in OPERATIONS

        if is_forced_equals:
            return ["="]

        if is_forced_digit:
            return DIGITS

        if can_be_equals:
            return DIGITS + OPERATIONS + ["="]

        return DIGITS + OPERATIONS


class Solutions:
    def __init__(self, num_chars):
        self.num_chars = num_chars
        self.solutions = []

    def generate_all_solutions(self, solution: Solution = None):
        """Generates a list of all syntactically correct solutions given
        starting characters"""

        if solution is None:
            solution = Solution(self.num_chars)

        # solution is full length, append!
        if solution.is_full:
            self.solutions.append(solution)

        # otherwise return list of possible solutions
        else:
            for option in solution.get_options_for_next_char():
                new_solution = Solution(self.num_chars, solution.chars + [option])
                self.generate_all_solutions(new_solution)

    @property
    def valid_solutions(self):
        return [solution for solution in self.solutions if solution.is_valid_solution]


def find_all_solutions():

    solutions = Solutions(num_chars=6)

    solutions.generate_all_solutions()

    valid_solutions = solutions.valid_solutions

    print("done")
    print(f"{len(valid_solutions)} valid solutions found")

    return valid_solutions


if __name__ == "__main__":
    solutions = find_all_solutions()

    solution_strs = [s.__str__() for s in solutions]

    outpath = Path("generated_solutions", "nerdle_solutions.txt")
    with open(outpath, "w") as file:
        file.write("\n".join(solution_strs))

    print(f"saved to {outpath}")
