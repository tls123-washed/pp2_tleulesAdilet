import os
from pathlib import Path


def main():
    path = Path(input("Path: ").strip()).expanduser()
    print("Exists:", os.access(path, os.F_OK))
    print("Readable:", os.access(path, os.R_OK))
    print("Writable:", os.access(path, os.W_OK))
    print("Executable / directory searchable:", os.access(path, os.X_OK))


if __name__ == "__main__":
    main()
