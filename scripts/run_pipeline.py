from __future__ import annotations

import subprocess
import sys


COMMANDS = [
    ["python", "scripts/prepare_catalog.py"],
    ["python", "scripts/build_embeddings.py", "--batch-size", "32"],
    ["python", "scripts/build_index.py"],
    ["python", "scripts/train_compatibility.py"],
]


def main() -> None:
    for command in COMMANDS:
        print(f"\nRunning: {' '.join(command)}")
        subprocess.run(command, check=True)


if __name__ == "__main__":
    sys.exit(main())
