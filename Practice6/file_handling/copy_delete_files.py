import shutil
from pathlib import Path
from tempfile import TemporaryDirectory


def main():
    with TemporaryDirectory() as folder:
        source = Path(folder) / "original.txt"
        copy = Path(folder) / "copy.txt"
        backup = Path(folder) / "backup.txt"
        source.write_text("Important sample data\n", encoding="utf-8")
        shutil.copy(source, copy)
        shutil.copy2(source, backup)  # Also attempts to preserve metadata.
        print("Copy:", copy.read_text(encoding="utf-8"))
        print("Backup:", backup.read_text(encoding="utf-8"))
        if copy.is_file():
            copy.unlink()
        print("Copy exists after deletion:", copy.exists())
        print("Backup still exists:", backup.exists())


if __name__ == "__main__":
    main()
