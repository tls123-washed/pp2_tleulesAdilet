class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Пополнение на {amount}. Новый баланс: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print(f"Отказано: недостаточно средств. Баланс: {self.balance}")
        else:
            self.balance -= amount
            print(f"Снято {amount}. Оставшийся баланс: {self.balance}")