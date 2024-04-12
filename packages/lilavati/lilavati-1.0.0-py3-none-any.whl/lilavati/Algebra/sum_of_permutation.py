from typing import List
from .permutation import *

def sum_of_permutation(number_list: List)->int:
    """
    Calculate the sum of all permutations of a given list of numbers.

    Parameters:
    number_list (List): List of numbers.

    Returns:
    int: The sum of all permutations.
    """
    number_sum=0
    for i in number_list:
        number_sum+=i
    one_num=int("1"*len(number_list))
    number_of_permutations=permutation(len(number_list),len(number_list))
    return ((number_of_permutations*number_sum)/len(number_list))*(one_num)

# Example usage:
# print(sum_of_permutation([1, 2, 3]))  # Output: 1332