#!/usr/bin/env python3
import random
from typing import List, Dict, Tuple

RANDOM_SEED = 18

PageRow = Dict[str, int]  # keys: 'Page','Loaded','LastRef','R','M'

def nru_class(row: PageRow) -> int:
    return 2 * row['R'] + row['M']

def fifo_victim(table: List[PageRow]) -> int:
    victim = min(table, key=lambda r: r['Loaded'])
    return victim['Page']

def lru_victim(table: List[PageRow]) -> int:
    victim = min(table, key=lambda r: r['LastRef'])
    return victim['Page']

def nru_victim(table: List[PageRow]) -> int:
    classes = [(nru_class(r), r['Page']) for r in table]
    min_class = min(c for c, _ in classes)
    candidates = [r for r in table if nru_class(r) == min_class]
    victim = min(candidates, key=lambda r: r['Page'])
    return victim['Page']

def second_chance_victim(table: List[PageRow]) -> int:
    queue = sorted([r.copy() for r in table], key=lambda r: r['Loaded'])
    N = len(queue)
    passes = 0
    while passes < 2 * N:
        first = queue[0]
        if first['R'] == 0:
            return first['Page']
        else:
            # give second chance
            first['R'] = 0
            queue = queue[1:] + [first]
        passes += 1
    # fallback
    return queue[0]['Page']

def print_table(table: List[PageRow], title: str = "Table") -> None:
    print(f"\n=== {title} ===")
    print(f"{'Page':>4} {'Loaded':>8} {'LastRef':>8} {'R':>3} {'M':>3}")
    for r in sorted(table, key=lambda x: x['Page']):
        print(f"{r['Page']:4} {r['Loaded']:8} {r['LastRef']:8} {r['R']:3} {r['M']:3}")

def compute_and_print_victims(table: List[PageRow]) -> None:
    print_table(table)
    print()
    print(f"a) NRU will replace page: {nru_victim(table)}")
    print(f"b) FIFO will replace page: {fifo_victim(table)}")
    print(f"c) LRU will replace page: {lru_victim(table)}")
    print(f"d) Second Chance will replace page: {second_chance_victim(table)}")
    print("-" * 40)

def make_random_table(num_pages: int = 5, loaded_max: int = 400, lastref_max: int = 500) -> List[PageRow]:
    rows = []
    for p in range(num_pages):
        loaded = random.randint(0, loaded_max)
        lastref = random.randint(loaded, lastref_max)  # ensure lastref >= loaded
        R = random.randint(0, 1)
        M = random.randint(0, 1)
        rows.append({'Page': p, 'Loaded': loaded, 'LastRef': lastref, 'R': R, 'M': M})
    return rows

def main():
    static_table = [
        {'Page': 0, 'Loaded': 126, 'LastRef': 280, 'R': 1, 'M': 0},
        {'Page': 1, 'Loaded': 230, 'LastRef': 265, 'R': 0, 'M': 1},
        {'Page': 2, 'Loaded': 140, 'LastRef': 270, 'R': 0, 'M': 0},
        {'Page': 3, 'Loaded': 110, 'LastRef': 285, 'R': 1, 'M': 1},
    ]
    print("STATIC EXAMPLE (from the prompt):")
    compute_and_print_victims(static_table)

    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)
        print(f"(Random table generated with seed={RANDOM_SEED})")
    else:
        print("(Random table generated with no fixed seed)")

    rand_table = make_random_table(num_pages=5)
    compute_and_print_victims(rand_table)

if __name__ == "__main__":
    main()