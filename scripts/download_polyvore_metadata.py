from __future__ import annotations

from pathlib import Path
import tarfile

import requests
from tqdm import tqdm


URL = "https://raw.githubusercontent.com/xthan/polyvore-dataset/master/polyvore.tar.gz"


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    raw_dir = root / "data" / "raw" / "polyvore"
    raw_dir.mkdir(parents=True, exist_ok=True)
    archive = raw_dir / "polyvore.tar.gz"

    if not archive.exists():
        with requests.get(URL, stream=True, timeout=60) as response:
            response.raise_for_status()
            total = int(response.headers.get("content-length", 0))
            with archive.open("wb") as f, tqdm(total=total, unit="B", unit_scale=True, desc="Polyvore metadata") as bar:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))

    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(raw_dir)
    print(f"Polyvore metadata extracted to {raw_dir}")


if __name__ == "__main__":
    main()
