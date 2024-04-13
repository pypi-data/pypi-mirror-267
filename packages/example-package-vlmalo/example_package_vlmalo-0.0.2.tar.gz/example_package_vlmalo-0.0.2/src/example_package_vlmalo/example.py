import math

def quadratic_formula(a, b, c):
    D = (b * b) - (4 * a * c)

    if D > 0:
        sol1 = (-b + math.sqrt(D)) / (2 * a)
        sol2 = (-b - math.sqrt(D)) / (2 * a)
        return sol1, sol2
    elif D == 0:
        sol = -b / (2 * a)
        return sol
    else:
        return None, "No real roots exist for the given coefficients."
