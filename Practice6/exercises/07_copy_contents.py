import shutil
from pathlib import Path


def main():
    source = Path(input("Source file path: ").strip()).expanduser()
    destination = Path(input("New destination file path: ").strip()).expanduser()
    try:
        # Binary mode also preserves non-text files exactly.
        # Open source first; x refuses to overwrite any existing destination.
        with open(source, "rb") as source_file:
            with open(destination, "xb") as destination_file:
                shutil.copyfileobj(source_file, destination_file)
        print("Copied to:", destination)
    except OSError as error:
        print("Copy failed:", error)


if __name__ == "__main__":
    main()
