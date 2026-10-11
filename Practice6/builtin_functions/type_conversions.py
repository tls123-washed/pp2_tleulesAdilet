def main():
    text = "42"
    number = int(text)
    print("type:", type(text), type(number))
    print("isinstance:", isinstance(number, int))
    print("float:", float("3.14"))
    print("str:", str(number))
    print("bool:", bool(0), bool(1), bool(""), bool("False"))
    print("list:", list((1, 2, 3)))
    print("tuple:", tuple([1, 2, 3]))
    print("set:", sorted(set([1, 1, 2, 3])))
    print("dict:", dict([("name", "Adilet"), ("score", 95)]))
    print("int from float:", int(3.9))  # Truncates toward zero.
    try:
        print(int("hello"))
    except ValueError:
        print("Cannot convert 'hello' to int.")


if __name__ == "__main__":
    main()
