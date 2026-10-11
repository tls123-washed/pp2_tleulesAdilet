import shutil
from pathlib import Path
from tempfile import TemporaryDirectory


def main():
    with TemporaryDirectory() as folder:
        root = Path(folder)
        source_dir = root / "source"
        target_dir = root / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        source = source_dir / "notes.txt"
        source.write_text("Python notes\n", encoding="utf-8")
        shutil.copy2(source, target_dir / "copy.txt")
        shutil.move(str(source), str(target_dir / "moved.txt"))
        print("Source entries:", list(source_dir.iterdir()))
        print("Target entries:", sorted(path.name for path in target_dir.iterdir()))
        shutil.copytree(target_dir, root / "target_backup")
        print("Copied directory:", (root / "target_backup").exists())


if __name__ == "__main__":
    main()
