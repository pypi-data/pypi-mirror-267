def permutation(n: int, r: int) -> int:
    """
    Calculate the number of permutations of n things taken r at a time (nPr).

    Parameters:
    n (int): Total number of items.
    r (int): Number of items to choose.

    Returns:
    int: The number of permutations.
    """
    if r > n:
        return 0
    if r == 0 or r == n:
        return 1

    product = 1
    for i in range(r):
        product = int(product) * int(n-i) # n * (n-1) * (n-2) * ... * (n-r+1)
    return product

# Example usage:
# print(permutation(10, 3))  # Output: 720