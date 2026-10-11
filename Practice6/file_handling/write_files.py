from pathlib import Path
from tempfile import TemporaryDirectory


def main():
    # All demo files live in a temporary folder.
    with TemporaryDirectory() as folder:
        path = Path(folder) / "sample.txt"
        with open(path, "w", encoding="utf-8") as file:
            file.write("Python files\nFirst line\n")
        with open(path, "a", encoding="utf-8") as file:
            file.write("Appended line\n")
        with open(path, "r", encoding="utf-8") as file:
            print(file.read())

        exclusive = Path(folder) / "new.txt"
        with open(exclusive, "x", encoding="utf-8") as file:
            file.write("Created only if the file does not exist.\n")
        try:
            with open(exclusive, "x", encoding="utf-8"):
                pass
        except FileExistsError:
            print("Mode x refuses to overwrite an existing file.")


if __name__ == "__main__":
    main()
