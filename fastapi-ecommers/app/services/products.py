import json
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "products.json"

def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"products.json not found at {DATA_FILE}")

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def fetch_all_products() -> List[Dict]:
    return load_products()
