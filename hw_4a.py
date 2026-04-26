import numpy as np
from scipy.integrate import quad

def rho(x):
    return -np.log(x)

def f0(x): return 1
def f1(x): return x
def f2(x): return x**2
def f3(x): return x**3
def f4(x): return x**4          # пример многочлена
def f5(x): return np.sin(x)     # функция варианта 5

functions = {
    "0": ("f0(x)=1", f0),
    "1": ("f1(x)=x", f1),
    "2": ("f2(x)=x^2", f2),
    "3": ("f3(x)=x^3", f3),
    "4": ("f4(x)=x^4", f4),
    "5": ("f5(x)=sin(x)", f5),
}

def moment(k, a, b):
    val, _ = quad(lambda x: (x**k) * rho(x), a, b, points=[0])
    return val

def exact_integral(func, a, b):
    val, _ = quad(lambda x: rho(x) * func(x), a, b, points=[0])
    return val

def build_iqf(nodes, a, b):
    N = len(nodes)

    # матрица Вандермонда: A1*x1^j + ... + AN*xN^j = mu_j
    V = np.array([[nodes[i]**j for i in range(N)] for j in range(N)], dtype=float)
    mu = np.array([moment(j, a, b) for j in range(N)], dtype=float)

    coeffs = np.linalg.solve(V, mu)
    return coeffs

def main():
    while True:
        print("\nВариант 5: rho(x) = -ln(x), f(x) = sin(x)")
        print("Рекомендуемый промежуток: [0, 1]")

        a = float(input("Введите a: "))
        b = float(input("Введите b: "))

        print("\nВыберите функцию:")
        for key, (name, _) in functions.items():
            print(f"{key}: {name}")

        choice = input("Ваш выбор: ")
        name, func = functions.get(choice, functions["5"])
        print(f"Выбрана функция: {name}")

        N = int(input("\nВведите количество узлов N: "))

        nodes = []
        print("Введите узлы:")
        for i in range(N):
            x = float(input(f"x[{i+1}] = "))
            nodes.append(x)

        nodes = np.array(nodes, dtype=float)

        if len(set(nodes)) != len(nodes):
            print("Ошибка: узлы должны быть попарно различными.")
            continue

        coeffs = build_iqf(nodes, a, b)

        print("\nУзлы и коэффициенты ИКФ:")
        for i in range(N):
            print(f"x{i+1} = {nodes[i]:.10f}, A{i+1} = {coeffs[i]:.10f}")

        # проверка точности на многочлене степени N-1: x^(N-1)
        test_func = lambda x: x**(N - 1)
        exact_test = exact_integral(test_func, a, b)
        approx_test = sum(coeffs[i] * test_func(nodes[i]) for i in range(N))

        print("\nПроверка точности на x^(N-1):")
        print(f"Точное значение      = {exact_test:.15f}")
        print(f"Приближенное значение = {approx_test:.15f}")
        print(f"Разность             = {abs(exact_test - approx_test):.3e}")

        approx = sum(coeffs[i] * func(nodes[i]) for i in range(N))
        exact = exact_integral(func, a, b)

        abs_err = abs(exact - approx)
        rel_err = abs_err / abs(exact) if exact != 0 else np.nan

        print("\nВычисление интеграла:")
        print(f"Приближенное значение = {approx:.15f}")
        print(f"Точное значение       = {exact:.15f}")
        print(f"Абсолютная погрешность = {abs_err:.3e}")
        print(f"Относительная погрешность = {rel_err:.3e}")

        again = input("\nПродолжить? да/нет: ").lower()
        if again not in ["да", "yes", "y", "д"]:
            break

if __name__ == "__main__":
    main()