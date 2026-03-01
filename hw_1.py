import math



def f(x):
    return x * math.sin(x) - 1

def df(x):
    return math.sin(x) + x * math.cos(x)

def d2f(x):
    return 2 * math.cos(x) - x * math.sin(x)


# ПРОЦЕДУРА ОТДЕЛЕНИЯ КОРНЕЙ

def separate_roots(A, B, N):
    h = (B - A) / N
    intervals = []
    x1 = A

    for i in range(N):
        x2 = x1 + h
        if f(x1) * f(x2) <= 0:
            intervals.append((x1, x2))
        x1 = x2

    print(f"\nНайдено {len(intervals)} отрезков перемены знака с шагом h = {h}\n")
    for i, (a, b) in enumerate(intervals):
        print(f"{i+1}: [{a}, {b}]")

    return intervals


# ===============================
# МЕТОД БИСЕКЦИИ
# ===============================

def bisection(a, b, eps):
    steps = 0
    while (b - a) > 2*eps:
        c = (a + b) / 2
        if f(a)*f(c) <= 0:
            b = c
        else:
            a = c
        steps += 1

    x = (a + b)/2
    return x, steps, abs(f(x))


# ===============================
# МЕТОД НЬЮТОНА
# ===============================

def newton(a, b, eps):
    x = (a + b)/2
    steps = 0

    while True:
        x_new = x - f(x)/df(x)
        steps += 1
        if abs(x_new - x) < eps:
            break
        x = x_new

    return x_new, steps, abs(f(x_new))


# ===============================
# МОДИФИЦИРОВАННЫЙ НЬЮТОН
# ===============================

def modified_newton(a, b, eps):
    x = (a + b)/2
    dfx0 = df(x)
    steps = 0

    while True:
        x_new = x - f(x)/dfx0
        steps += 1
        if abs(x_new - x) < eps:
            break
        x = x_new

    return x_new, steps, abs(f(x_new))


# ===============================
# МЕТОД СЕКУЩИХ
# ===============================

def secant(a, b, eps):
    x0 = a
    x1 = b
    steps = 0

    while True:
        x2 = x1 - f(x1)*(x1-x0)/(f(x1)-f(x0))
        steps += 1
        if abs(x2 - x1) < eps:
            break
        x0, x1 = x1, x2

    return x2, steps, abs(f(x2))


# ===============================
# ЗАДАЧА О ПОГРУЖЕНИИ ШАРА
# ===============================

def sphere_problem():
    r = float(input("Введите радиус шара (м): "))

    densities = {
        "Пробка": 0.25,
        "Бамбук": 0.4,
        "Сосна": 0.5,
        "Кедр": 0.55,
        "Дуб": 0.7,
        "Бук": 0.75,
        "Красное дерево": 0.8,
        "Тиковое дерево": 0.85,
        "Парафин": 0.9,
        "Полиэтилен": 0.92,
        "Пчелиный воск": 0.95
    }

    print("\nВещество | Плотность | Глубина погружения (м)")
    print("-----------------------------------------------")

    for material, rho in densities.items():

        def g(d):
            return (math.pi*d**2*(3*r - d)/3) / ((4/3)*math.pi*r**3) - rho

        a, b = 0, 2*r
        eps = 1e-6

        while (b - a) > 2*eps:
            c = (a + b)/2
            if g(a)*g(c) <= 0:
                b = c
            else:
                a = c

        d = (a + b)/2

        print(f"{material:15} | {rho:8} | {d:.6f}")


# ===============================
# ГЛАВНОЕ МЕНЮ
# ===============================

def main():
    while True:
        print("\n1 — Тестовая задача")
        print("2 — Задача о погружении шара")
        print("0 — Выход")

        choice = input("Выберите пункт: ")

        if choice == "1":
            A = float(input("Введите A: "))
            B = float(input("Введите B: "))
            N = int(input("Введите N: "))

            intervals = separate_roots(A, B, N)

            if len(intervals) == 0:
                continue

            index = int(input("\nВыберите номер отрезка: ")) - 1
            eps = float(input("Введите точность eps: "))

            a, b = intervals[index]

            print("\nМетод                Шаги        Корень              Невязка")
            print("-----------------------------------------------------------------")

            x, s, r = bisection(a, b, eps)
            print(f"Бисекция             {s:5}   {x:.15f}   {r:.2e}")

            x, s, r = newton(a, b, eps)
            print(f"Ньютон               {s:5}   {x:.15f}   {r:.2e}")

            x, s, r = modified_newton(a, b, eps)
            print(f"Модиф. Ньютон        {s:5}   {x:.15f}   {r:.2e}")

            x, s, r = secant(a, b, eps)
            print(f"Секущие              {s:5}   {x:.15f}   {r:.2e}")

        elif choice == "2":
            sphere_problem()

        elif choice == "0":
            break


if __name__ == "__main__":
    main()