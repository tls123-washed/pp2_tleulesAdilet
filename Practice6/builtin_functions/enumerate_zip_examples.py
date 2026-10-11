def main():
    names = ["Adilet", "Dana", "Arman"]
    scores = [95, 88, 91]
    for index, name in enumerate(names, start=1):
        print(index, name)
    for name, score in zip(names, scores):
        print(name, score)
    print("Pairs:", list(zip(names, scores)))
    print("Highest score first:", sorted(zip(names, scores), key=lambda pair: pair[1], reverse=True))
    # zip stops at the shortest input by default.
    print("Unequal lengths:", list(zip(names, [100])))


if __name__ == "__main__":
    main()
