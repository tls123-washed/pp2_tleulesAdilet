
#Exercise 1: squares up to N
def squares_up_to(n):
    for i in range(1, n + 1):
        yield i * i


print(list(squares_up_to(5)))    # [1, 4, 9, 16, 25]


#Exercise 2: even numbers
def evens(n):
    for i in range(0, n + 1, 2):
        yield i


n = int(input("Enter n: "))
print(",".join(str(x) for x in evens(n)))


#Exercise 3: divisible by 3 and 4 in 0..n
def divisible_by_3_and_4(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


print(list(divisible_by_3_and_4(50)))   # [0, 12, 24, 36, 48]


#Exercise 4: squares from a to b
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


for value in squares(3, 7):
    print(value) # 9 16 25 36 49


#Exercise 5: n down to 0
def countdown(n):
    while n >= 0:
        yield n
        n -= 1


print(list(countdown(5))) #[5, 4, 3, 2, 1, 0]
