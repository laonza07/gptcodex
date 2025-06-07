import argparse
import math
from typing import List, Tuple

def load_ppm(path: str) -> Tuple[int, int, int, List[Tuple[int, int, int]]]:
    """Load a P3 PPM image file.

    Returns width, height, maxval and a list of RGB pixel tuples.
    Only the ASCII P3 format is supported to avoid external dependencies.
    """
    tokens: List[str] = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            tokens.extend(line.split())

    if not tokens or tokens[0] != 'P3':
        raise ValueError('Unsupported or missing PPM header')
    try:
        width = int(tokens[1])
        height = int(tokens[2])
        maxval = int(tokens[3])
    except (IndexError, ValueError) as e:
        raise ValueError('Invalid PPM header') from e

    values = list(map(int, tokens[4:]))
    expected = width * height * 3
    if len(values) != expected:
        raise ValueError(f'Expected {expected} color values, got {len(values)}')

    pixels = [tuple(values[i:i+3]) for i in range(0, expected, 3)]
    return width, height, maxval, pixels

def euclidean_distance(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def mean_color_difference(p1: List[Tuple[int, int, int]], p2: List[Tuple[int, int, int]]) -> float:
    if len(p1) != len(p2):
        raise ValueError('Images must be the same size for comparison')
    total = 0.0
    for c1, c2 in zip(p1, p2):
        total += euclidean_distance(c1, c2)
    return total / len(p1)

def verify_patterns(ref_path: str, cmp_path: str, threshold: float = 5.0) -> float:
    r_w, r_h, _, ref_pixels = load_ppm(ref_path)
    c_w, c_h, _, cmp_pixels = load_ppm(cmp_path)
    if (r_w, r_h) != (c_w, c_h):
        raise ValueError('Reference and comparison images must have the same dimensions')
    diff = mean_color_difference(ref_pixels, cmp_pixels)
    if diff <= threshold:
        print(f'Match: mean color difference {diff:.2f} \u2264 {threshold}')
    else:
        print(f'Difference detected: mean color difference {diff:.2f} > {threshold}')
    return diff

def main() -> None:
    parser = argparse.ArgumentParser(description='Verify color similarity between two PPM patterns')
    parser.add_argument('reference', help='Reference PPM image path')
    parser.add_argument('comparison', help='Comparison PPM image path')
    parser.add_argument('--threshold', type=float, default=5.0, help='Allowed mean color distance (default: 5.0)')
    args = parser.parse_args()
    try:
        verify_patterns(args.reference, args.comparison, args.threshold)
    except Exception as e:
        parser.error(str(e))

if __name__ == '__main__':
    main()
