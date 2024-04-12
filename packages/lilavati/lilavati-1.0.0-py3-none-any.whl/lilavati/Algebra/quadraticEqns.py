def quadratic(b, c):
    if b > 0:
        res = ((c + (b / 2) ** 2) ** 0.5 - b / 2) ** 2
    elif b < 0:
        res = ((c + ((-b) / 2) ** 2) ** 0.5 + (-b) / 2) ** 2
    return res ** 0.5