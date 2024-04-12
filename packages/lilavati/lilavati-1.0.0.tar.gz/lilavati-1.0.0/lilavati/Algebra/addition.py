def add(*args):
    max_length = max(len(str(num)) for num in args)
    sum_columns = [[int(str(num)[::-1][i]) if len(str(num)) > i else 0 for num in args] for i in range(max_length)]
    column_sums = [sum(column) for column in sum_columns]       #[18,15,12]

    res = 0
    for i in range(len(column_sums)):
        res += column_sums[i]*10**(i)
    return res

