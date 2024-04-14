def fact(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers!")
    elif n < 2:
        return 1
    else:
        return n * fact(n-1)