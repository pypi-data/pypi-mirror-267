from .fib_number import recurring_fibonacci_number


def calculate_numbers(numbers: list[int]) -> list[int]:
    return [recurring_fibonacci_number(n) for n in numbers]
