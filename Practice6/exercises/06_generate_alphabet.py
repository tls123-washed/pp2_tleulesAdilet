import string
from pathlib import Path


def main():
    folder = Path(input("Output directory: ").strip()).expanduser()
    created = 0
    try:
        folder.mkdir(parents=True, exist_ok=True)
        for letter in string.ascii_uppercase:
            path = folder / (letter + ".txt")
            try:
                with open(path, "x", encoding="utf-8") as file:
                    file.write(letter + "\n")
                created += 1
            except FileExistsError:
                print("Already exists, skipped:", path.name)
        print("New files created:", created)
    except OSError as error:
        print("Cannot generate files:", error)


if __name__ == "__main__":
    main()
