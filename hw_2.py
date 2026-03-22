import math, random

# Вариант 5 (по PDF):
# f(x)=1-exp(-2x), a=-0.5, b=1, m+1=51, n=8
def f(x):
    return 1 - math.exp(-2 * x)

def make_nodes(m1, a, b, mode):
    if mode == "2":  # случайные попарно различные
        xs = sorted(random.sample([a + (b - a) * i / 100000 for i in range(100001)], m1))
    else:  # равноотстоящие
        h = (b - a) / (m1 - 1)
        xs = [a + i * h for i in range(m1)]
    ys = [f(x) for x in xs]
    return xs, ys

def lagrange(x, xs, ys):
    n = len(xs)
    p = 0.0
    s = 0.0
    for i in range(n):
        li = 1.0
        for j in range(n):
            if i != j:
                li *= (x - xs[j]) / (xs[i] - xs[j])
        s += li
        p += ys[i] * li
    print(f"Контроль (сумма коэффициентов Лагранжа) = {s:.12f}")
    return p

def newton(x, xs, ys):
    n = len(xs)
    dd = [row[:] for row in [[0.0] * n for _ in range(n)]]
    for i in range(n):
        dd[i][0] = ys[i]
    for j in range(1, n):
        for i in range(n - j):
            dd[i][j] = (dd[i + 1][j - 1] - dd[i][j - 1]) / (xs[i + j] - xs[i])

    print("\nТаблица разделённых разностей:")
    for i in range(n):
        print(f"{xs[i]:>10.6f}", end=" | ")
        for j in range(n - i):
            print(f"{dd[i][j]:>14.10f}", end=" ")
        print()

    p = dd[0][0]
    w = 1.0
    for j in range(1, n):
        w *= (x - xs[j - 1])
        p += dd[0][j] * w
    return p

def main():
    print("ЗАДАЧА АЛГЕБРАИЧЕСКОГО ИНТЕРПОЛИРОВАНИЯ")
    print("Вариант 5")
    print("f(x)=1-exp(-2x)")

    m1 = int(input("Введите m+1 [51]: ") or 51)
    while m1 < 2:
        m1 = int(input("m+1 должно быть >1. Введите снова: "))
    m = m1 - 1

    while True:
        a = float(input("Введите a [-0.5]: ") or -0.5)
        b = float(input("Введите b [1]: ") or 1)
        if a < b:
            break
        print("Ошибка: a должно быть меньше b")

    mode = input("1 - равноотстоящие, 2 - случайные [1]: ") or "1"
    xs, ys = make_nodes(m1, a, b, mode)

    print("\nИсходная таблица:")
    print(" k |      z_k      |      f(z_k)")
    for i in range(m1):
        print(f"{i:2d} | {xs[i]:12.8f} | {ys[i]:14.10f}")

    while True:
        x = float(input("\nВведите x: "))

        while True:
            n = int(input(f"Введите n (n≤{m}) [8]: ") or 8)
            if n <= m:
                break
            print("Введено недопустимое значение n")

        data = sorted(zip(xs, ys), key=lambda t: abs(t[0] - x))
        print("\nОтсортированная таблица:")
        print(" i |     x_i       |      f(x_i)      |   |x_i-x|")
        for i, (xi, yi) in enumerate(data):
            print(f"{i:2d} | {xi:12.8f} | {yi:14.10f} | {abs(xi-x):10.8f}")

        use = data[:n + 1]
        xk = [t[0] for t in use]
        yk = [t[1] for t in use]

        print("\nУзлы для Pn(x):")
        for i in range(n + 1):
            print(f"x{i} = {xk[i]:.8f}, f = {yk[i]:.10f}")

        fx = f(x)
        pl = lagrange(x, xk, yk)
        pn = newton(x, xk, yk)

        print("\nРЕЗУЛЬТАТЫ:")
        print(f"f({x})     = {fx:.12f}")
        print(f"P{n}_L({x}) = {pl:.12f}")
        print(f"|f(x)-P_L| = {abs(fx - pl):.12e}")
        print(f"P{n}_N({x}) = {pn:.12f}")
        print(f"|f(x)-P_N| = {abs(fx - pn):.12e}")
        print(f"|P_L-P_N|  = {abs(pl - pn):.12e}")

        if input("\nВведите q для выхода, иначе продолжить: ").lower() == "q":
            break

if __name__ == "__main__":
    main()