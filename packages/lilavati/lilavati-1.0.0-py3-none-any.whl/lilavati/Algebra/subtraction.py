def subtract(a, b):
    # Convert numbers to lists of digits
    num1 = [int(digit) for digit in str(a)]
    num2 = [int(digit) for digit in str(b)]

    # Ensure num1 is larger or equal to num2
    if len(num1) < len(num2):
        num1, num2 = num2, num1

    # Pad num2 with leading zeros if needed
    num2 = [0] * (len(num1) - len(num2)) + num2

    # Perform subtraction
    result = []
    borrow = 0
    for digit1, digit2 in zip(num1[::-1], num2[::-1]):
        difference = digit1 - digit2 - borrow
        if difference < 0:
            difference += 10
            borrow = 1
        else:
            borrow = 0
        result.insert(0, difference)

    # Remove leading zeros
    while result[0] == 0:
        result.pop(0)

    result_int = int(''.join(map(str, result)))

    return result_int
