import math

# ==========================================================
# ФУНКЦИИ И ИХ ТОЧНЫЕ ПРОИЗВОДНЫЕ
# ==========================================================

FUNCTIONS = {
    1: ("f1(x) = 2x^2 - 3x + 1",
        lambda x: 2*x**2 - 3*x + 1,
        lambda x: 4*x - 3,
        lambda x: 4.0),
    2: ("f2(x) = x^3 - 2x^2 + x - 5",
        lambda x: x**3 - 2*x**2 + x - 5,
        lambda x: 3*x**2 - 4*x + 1,
        lambda x: 6*x - 4),
    3: ("f3(x) = e^(4x)",
        lambda x: math.exp(4*x),
        lambda x: 4*math.exp(4*x),
        lambda x: 16*math.exp(4*x)),
    4: ("f4(x) = sin(2x) - 1.25x^2 + 0.35",
        lambda x: math.sin(2*x) - 1.25*x**2 + 0.35,
        lambda x: 2*math.cos(2*x) - 2.5*x,
        lambda x: -4*math.sin(2*x) - 2.5),
}

# ==========================================================
# ФОРМУЛЫ ЧИСЛЕННОГО ДИФФЕРЕНЦИРОВАНИЯ
# ==========================================================

# --- Первая производная O(h^2) ---
def d1_h2(y, h):
    m = len(y) - 1
    r = [0.0] * (m + 1)
    r[0] = (-3*y[0] + 4*y[1] - y[2]) / (2*h)                      # (4)
    for k in range(1, m):
        r[k] = (y[k+1] - y[k-1]) / (2*h)                          # (3)
    r[m] = (3*y[m] - 4*y[m-1] + y[m-2]) / (2*h)                   # (5)
    return r

# --- Первая производная O(h^4) ---
def d1_h4(y, h):
    m = len(y) - 1
    r = [0.0] * (m + 1)
    r[0] = (-25*y[0] + 48*y[1] - 36*y[2] + 16*y[3] - 3*y[4]) / (12*h)          # (7)
    r[1] = (-3*y[0] - 10*y[1] + 18*y[2] - 6*y[3] + y[4]) / (12*h)              # (8)
    for k in range(2, m - 1):
        r[k] = (y[k-2] - 8*y[k-1] + 8*y[k+1] - y[k+2]) / (12*h)               # (9)
    r[m-1] = (3*y[m] + 10*y[m-1] - 18*y[m-2] + 6*y[m-3] - y[m-4]) / (12*h)    # (10)
    r[m]   = (25*y[m] - 48*y[m-1] + 36*y[m-2] - 16*y[m-3] + 3*y[m-4]) / (12*h)# (11)
    return r

# --- Вторая производная O(h^2) ---
def d2_h2(y, h):
    m = len(y) - 1
    r = [0.0] * (m + 1)
    r[0] = (2*y[0] - 5*y[1] + 4*y[2] - y[3]) / h**2                # (12)
    for k in range(1, m):
        r[k] = (y[k+1] - 2*y[k] + y[k-1]) / h**2                   # (6)
    r[m] = (2*y[m] - 5*y[m-1] + 4*y[m-2] - y[m-3]) / h**2          # (13)
    return r

# ==========================================================
# ВЫВОД ТАБЛИЦЫ
# ==========================================================

def print_table(x, y, f_d1, f_d2):
    m = len(x) - 1
    d1e = [f_d1(xk) for xk in x]
    d2e = [f_d2(xk) for xk in x]
    r1  = d1_h2(y, x[1]-x[0])
    r2  = d1_h4(y, x[1]-x[0])
    r3  = d2_h2(y, x[1]-x[0])

    hdrs = ["k","x_k","y_k","f'_T","f'~O(h2)","|err|","f'~O(h4)","|err|","f''_T","f''~O(h2)","|err|"]
    ws   = [4, 14, 16, 14, 14, 12, 14, 12, 14, 14, 12]
    print("\n" + "".join(h.ljust(w) for h, w in zip(hdrs, ws)))
    print("-" * sum(ws))
    for k in range(m + 1):
        row = [str(k), f"{x[k]:.8f}", f"{y[k]:.8f}",
               f"{d1e[k]:.8f}", f"{r1[k]:.8f}", f"{abs(r1[k]-d1e[k]):.2e}",
               f"{r2[k]:.8f}", f"{abs(r2[k]-d1e[k]):.2e}",
               f"{d2e[k]:.8f}", f"{r3[k]:.8f}", f"{abs(r3[k]-d2e[k]):.2e}"]
        print("".join(v.ljust(w) for v, w in zip(row, ws)))

# ==========================================================
# ПОДБОР ОПТИМАЛЬНОГО ШАГА
# ==========================================================

def optimal_step(f, d1_exact, x0, h0, n=8):
    exact = d1_exact(x0)
    print(f"\nПодбор оптимального шага, x={x0}, f'(x)={exact:.10f}")
    print(f"{'№':<4}{'h':<14}{'f\\':<18}{'|err|':<18}")
    best_h, best_err = h0, float("inf")
    h = h0
    for i in range(n):
        apx = (-3*f(x0) + 4*f(x0+h) - f(x0+2*h)) / (2*h)
        err = abs(apx - exact)
        print(f"{i+1:<4}{h:<14.8f}{apx:<18.10f}{err:<18.2e}")
        if err < best_err:
            best_err, best_h = err, h
        h /= 2
    print(f"\nЛучший шаг: h={best_h}, min погрешность={best_err:.2e}")

# ==========================================================
# ГЛАВНОЕ МЕНЮ
# ==========================================================

def input_float(prompt):
    while True:
        try: return float(input(prompt))
        except ValueError: print("Ошибка: введите число.")

def input_int(prompt, mn=None):
    while True:
        try:
            v = int(input(prompt))
            if mn is not None and v < mn:
                print(f"Нужно >= {mn}.")
            else:
                return v
        except ValueError: print("Ошибка: введите целое число.")

def main():
    print("=== Задание 3. Численное дифференцирование ===")
    while True:
        print("\nВыберите функцию:")
        for k, v in FUNCTIONS.items(): print(f"  {k}. {v[0]}")
        name, f, d1, d2 = FUNCTIONS[input_int("Номер (1-4): ", 1)]
        print(f"Выбрана: {name}")

        m  = input_int("m (точек будет m+1, нужно m>=4): ", 4)
        x0 = input_float("x0: ")
        h  = input_float("h > 0: ")
        while h <= 0:
            print("h должен быть > 0.")
            h = input_float("h > 0: ")

        x = [x0 + k*h for k in range(m+1)]
        y = [f(xk) for xk in x]

        print("\nТаблица значений:")
        print(f"{'k':<4}{'x_k':<16}{'y_k'}")
        for k in range(m+1):
            print(f"{k:<4}{x[k]:<16.8f}{y[k]:.8f}")

        print_table(x, y, d1, d2)

        if input("\nПодобрать оптимальный шаг? (y/n): ").strip().lower() == 'y':
            xp = input_float("Точка x: ")
            h0 = input_float("Начальный шаг h0 > 0: ")
            while h0 <= 0:
                print("h0 должен быть > 0.")
                h0 = input_float("h0 > 0: ")
            optimal_step(f, d1, xp, h0)

        if input("\nНовый расчёт? (y/n): ").strip().lower() != 'y':
            print("Завершено.")
            break

if __name__ == "__main__":
    main()