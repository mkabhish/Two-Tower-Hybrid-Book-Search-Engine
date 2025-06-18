import csv
from typing import List, Dict

PRODUCTS_CSV = "products_sample.csv"

def load_products(csv_path: str = PRODUCTS_CSV) -> List[Dict]:
    products = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            products.append(row)
    return products 