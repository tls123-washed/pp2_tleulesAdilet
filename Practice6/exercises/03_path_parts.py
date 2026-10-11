from pathlib import Path


def main():
    path = Path(input("Path: ").strip()).expanduser()
    if path.exists():
        print("Path exists.")
        print("Filename / last component:", path.name)
        print("Directory portion:", path.parent)
        print("Absolute path:", path.absolute())
    else:
        print("Path does not exist.")


if __name__ == "__main__":
    main()
