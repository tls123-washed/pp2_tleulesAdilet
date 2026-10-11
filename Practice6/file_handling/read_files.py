from pathlib import Path
from tempfile import TemporaryDirectory


def main():
    with TemporaryDirectory() as folder:
        path = Path(folder) / "sample.txt"
        path.write_text("Adilet\nPython\nPractice 6\n", encoding="utf-8")

        # Reopen the file to reset its reading position each time.
        with open(path, "r", encoding="utf-8") as file:
            print("read():")
            print(file.read())
        with open(path, "r", encoding="utf-8") as file:
            print("readline():", file.readline().rstrip("\n"))
        with open(path, "r", encoding="utf-8") as file:
            print("readlines():", file.readlines())
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                print("Iteration:", line.rstrip("\n"))


if __name__ == "__main__":
    main()
