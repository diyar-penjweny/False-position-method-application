def f(x):
    return ((x**3)-(4*x)-9)

def falsiPosition(a,b,E):
    counter = 0
    if f(a)*f(b) > 0:
        print(f"There is no number between {a} and {b} that makes the function zero")
        return None
    else:
        while abs(b - a) > E:
            counter += 1
            mid = (a * f(b) - b * f(a)) / (f(b) - f(a))

            if f(mid) == 0:
                return mid
            elif f(a) * f(mid) > 0:
                a = mid
            else:
                b = mid

            if counter == 1000:
                return mid, "Reached iteration limit (1000)"  # Fixed return

        return mid

print(falsiPosition(2, 3, 0.00001))