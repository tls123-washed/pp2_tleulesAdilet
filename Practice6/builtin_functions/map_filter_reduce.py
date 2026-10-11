from functools import reduce


def main():
    numbers = [1, 2, 3, 4, 5]
    squares = list(map(lambda number: number ** 2, numbers))
    even = list(filter(lambda number: number % 2 == 0, numbers))
    product = reduce(lambda result, number: result * number, numbers, 1)
    print("Numbers:", numbers)
    print("Squares:", squares)
    print("Even:", even)
    print("Product:", product)
    print("Length:", len(numbers))
    print("Sum:", sum(numbers))
    print("Minimum:", min(numbers))
    print("Maximum:", max(numbers))
    print("Sorted descending:", sorted(numbers, reverse=True))


if __name__ == "__main__":
    main()
