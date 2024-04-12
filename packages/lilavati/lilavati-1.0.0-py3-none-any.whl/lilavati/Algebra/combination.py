def combination(n: int, r: int) -> int:
    """
    Calculate the number of combinations of n things taken r at a time (nCr).

    Parameters:
    n (int): Total number of items.
    r (int): Number of items to choose.

    Returns:
    int: The number of combinations.
    """
    if r > n:
        return 0
    if r == 0 or r == n:
        return 1

    product = 1
    for i in range(1, r + 1):
        product *= n - i + 1
        product //= i

    return product

# Example usage:
# print(combination(5, 3))  # Output: 10