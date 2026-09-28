import itertools
import math
import random

# 1. Граммы в унции
def grams_to_ounces(grams):
    return 28.3495231 * grams

# 2. Фаренгейты в Цельсии
def fahrenheit_to_celsius(f):
    return (5 / 9) * (f - 32)

# 3. Головоломка с курами и кроликами (heads=35, legs=94)
# rabbits + chickens = heads
# 4*rabbits + 2*chickens = legs  =>  2*rabbits = legs - 2*heads
def solve(numheads, numlegs):
    for chickens in range(numheads + 1):
        rabbits = numheads - chickens
        if 2 * chickens + 4 * rabbits == numlegs:
            return chickens, rabbits
    return None, None

# 4. Фильтр простых чисел из списка
def filter_prime(numbers):
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    return [x for x in numbers if is_prime(x)]

# 5. Все перестановки строки
def print_permutations(s):
    perms = [''.join(p) for p in itertools.permutations(s)]
    print(perms)

# 6. Разворот порядка слов в предложении
def reverse_words(sentence):
    words = sentence.split()
    return " ".join(reversed(words))

# 7. Две тройки подряд (has_33)
def has_33(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 3 and nums[i + 1] == 3:
            return True
    return False

# 8. Код агента 007 по порядку (spy_game)
def spy_game(nums):
    code = [0, 0, 7]
    for n in nums:
        if n == code[0]:
            code.pop(0)
            if not code:
                return True
    return False

# 9. Объём сферы: V = 4/3 * pi * r^3
def sphere_volume(radius):
    return (4 / 3) * math.pi * (radius ** 3)

# 10. Уникальные элементы без использования set()
def unique_elements(lst):
    unique = []
    for item in lst:
        if item not in unique:
            unique.append(item)
    return unique

# 11. Проверка на палиндром
def is_palindrome(text):
    clean_text = "".join(text.lower().split())
    return clean_text == clean_text[::-1]

# 12. Вывод гистограммы
def histogram(lst):
    for count in lst:
        print('*' * count)

# 13. Игра "Угадай число"
def guess_the_number():
    target = random.randint(1, 20)
    print("Hello! What is your name?")
    name = input()
    print(f"\nWell, {name}, I am thinking of a number between 1 and 20.")
    
    attempts = 0
    while True:
        print("Take a guess.")
        guess = int(input())
        attempts += 1
        
        if guess < target:
            print("Your guess is too low.")
        elif guess > target:
            print("Your guess is too high.")
        else:
            print(f"Good job, {name}! You guessed my number in {attempts} guesses!")
            break