import argparse
from io import TextIOWrapper
from pathlib import Path

def main():
    args = parse_args()
    if args.action == "compress":
        compress()
    elif args.action == "decompress":
        decompress()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compress or decompress a project")
    parser.add_argument("action", type=str, help="Action to perform: compress or decompress")
    return parser.parse_args()

def compress():
    project_path = Path("./Project")
    output_file = open("Project.txt", "w")
    compress_helper(project_path, output_file)
    output_file.close()
    
def compress_helper(parent: Path, output_file: TextIOWrapper):
    for item in parent.iterdir():
        if item.name.startswith("."):
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
