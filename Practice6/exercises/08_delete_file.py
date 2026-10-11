import os
from pathlib import Path


def main():
    path = Path(input("File path to delete: ").strip()).expanduser()
    if not path.exists():
        print("Path does not exist.")
        return
    if path.is_symlink() or not path.is_file():
        print("Please specify a regular file, not a directory or symbolic link.")
        return

    print("Readable:", os.access(path, os.R_OK))
    print("Writable:", os.access(path, os.W_OK))
    print("Parent writable:", os.access(path.parent, os.W_OK))
    print("Parent searchable:", os.access(path.parent, os.X_OK))
    # Permission checks are advisory; the actual operation may still fail.
    print("Selected file:", path.absolute())
    if input("Type DELETE to confirm: ").strip() != "DELETE":
        print("Deletion cancelled.")
        return
    try:
        path.unlink()
        print("File deleted.")
    except OSError as error:
        print("Cannot delete file:", error)


if __name__ == "__main__":
    main()
