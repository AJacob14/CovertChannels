import sys
import json
from datetime import datetime
from pathlib import Path

def main(given_path: str):
    path = Path(given_path)
    if path.is_file():
        files = [path]
    else:
        files = list(path.rglob("*"))
    
    bigrams: dict[str, int] = {}
    for file in files:
        try:
            with file.open("rb") as f:
                data = f.read()
        except Exception as e:
            print(f"Error reading file {file}: {e}")
            continue
        for i in range(len(data) - 1):
            bigram = data[i:i+2]
            bigram_str = bigram.hex()
            if bigram_str in bigrams:
                bigrams[bigram_str] += 1
            else:
                bigrams[bigram_str] = 1

    out_path = Path("./Misc/Data")
    out_path.mkdir(exist_ok=True, parents=True)
    out_file = out_path / f"{datetime.now().isoformat().replace(':', '-')}.json"
    with out_file.open("w") as f:
        json.dump(bigrams, f, indent=4)

if __name__ == "__main__":
    main(sys.argv[1])
