import os
from pathlib import Path
from tempfile import TemporaryDirectory


def main():
    original = os.getcwd()
    with TemporaryDirectory() as folder:
        root = Path(folder)
        os.mkdir(root / "empty")
        os.makedirs(root / "course" / "notes", exist_ok=True)
        (root / "course" / "notes" / "lesson.txt").write_text("Lesson\n", encoding="utf-8")
        (root / "data.csv").write_text("name,score\nAdilet,95\n", encoding="utf-8")
        print("Entries:", sorted(os.listdir(root)))
        print("Text files, including subfolders:")
        for path in sorted(root.rglob("*.txt")):
            print(path.relative_to(root))
        try:
            os.chdir(root)
            print("Current working directory:", os.getcwd())
        finally:
            os.chdir(original)  # Restore before cleaning up the demo folder.
        os.rmdir(root / "empty")  # Only works for empty directories.
        print("After rmdir:", sorted(os.listdir(root)))


if __name__ == "__main__":
    main()
