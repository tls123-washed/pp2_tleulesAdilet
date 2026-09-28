numbers = (list(input("Введите ваши числа: ")))
def largest():
    current = 0
    for n in numbers:
        if(n > current):
            current += n

lar = largest()
print(lar)