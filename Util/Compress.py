"""
    Compress/decompress a project directory into a single text file.
"""
import argparse
from pathlib import Path
from typing import TextIO


def main():
    args = parse_args()
    if args.action == "compress":
        compress()
    elif args.action == "decompress":
        decompress()


def parse_args() -> argparse.Namespace:
    """
        Parse the command line arguments.
    """
    parser = argparse.ArgumentParser(description="Compress or decompress a project")
    parser.add_argument("action", type=str, help="Action to perform: compress or decompress")
    return parser.parse_args()


def compress():
    """
        Compress the project directory into a single text file.
    """
    project_path = Path(".")
    output_file = open("Project.txt", "w")
    compress_helper(project_path, output_file)
    output_file.close()


def compress_helper(parent: Path, output_file: TextIO):
    """
        Helper function to compress the project directory into a single text file.
    :param parent: Directory to compress
    :param output_file: Output file to write the compressed data to
    """
    for item in parent.iterdir():
        if item.name.startswith(".") or item.name in ("__pycache__", "venv", "Project.txt"):
            continue
        if item.is_dir():
            print(f"Compressing {item.name}")
            compress_helper(item, output_file)
            continue
        print(item)
        output_file.write(f"========== {str(item)}\n")
        with open(item, "r") as file:
            content = file.read()
        if content and content[-1] != "\n":
            content += "\n"
        output_file.write(content)


def decompress():
    """
        Decompress the project text file into the project directory.
    """
    output_path = Path("./Decompressed")
    with open("Project.txt", "r") as input_file:
        data = input_file.read()

    files = data.split("========== ")[1:]
    for file in files:
        file = file.split("\n", 1)
        file_path = output_path / file[0]
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w") as output_file:
            output_file.write(file[1])


if __name__ == "__main__":
    main()
