from pathlib import Path


def main():
    path = Path(input("Text file path: ").strip()).expanduser()
    try:
        with open(path, "r", encoding="utf-8") as file:
            count = sum(1 for line in file)
        print("Number of lines:", count)
    except (OSError, UnicodeError) as error:
        print("Cannot read file:", error)


if __name__ == "__main__":
    main()
