from pathlib import Path


def main():
    path = Path(input("Directory path: ").strip()).expanduser()
    try:
        entries = sorted(path.iterdir())
        print("Directories:", [item.name for item in entries if item.is_dir()])
        print("Files:", [item.name for item in entries if item.is_file()])
        print("All entries:", [item.name for item in entries])
    except OSError as error:
        print("Cannot list directory:", error)


if __name__ == "__main__":
    main()
