from pathlib import Path


def main():
    path = Path(input("New output file path: ").strip()).expanduser()
    items = input("List items separated by commas: ").split(",")
    try:
        # x protects an existing file from accidental replacement.
        with open(path, "x", encoding="utf-8") as file:
            for item in items:
                file.write(item.strip() + "\n")
        print("List written to:", path)
    except OSError as error:
        print("Cannot write file:", error)


if __name__ == "__main__":
    main()
