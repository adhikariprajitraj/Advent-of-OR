def is_magic_number(number):
    digits = str(number)
    n = len(digits)

    # Rule 1: all digits must be unique
    if len(set(digits)) != n:
        return False

    visited = [False] * n
    position = 0

    # We must visit exactly n digits
    for _ in range(n):
        if visited[position]:
            return False

        visited[position] = True
        step = int(digits[position])
        position = (position + step) % n

    # Must end back at the first digit
    return position == 0


A, B = map(int, input().split())
found = False

for num in range(A, B + 1):
    if is_magic_number(num):
        print(num)
        found = True

if not found:
    print(-1)

