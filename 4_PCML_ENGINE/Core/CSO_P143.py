# --- CSO_P143.py ---
# Caterpillar's Command: [Code-The-Inverse-Oracle] (from prompt 143)
# Timestamp: 2024-05-22 03:30:00 UTC
# Applicable Rules: All. The Inverse Oracle - A Geometric Reconstructor.

import numpy as np
import argparse
import math
from itertools import combinations

def generate_pythagorean_hypotenuses(limit):
    """Generates a set of unique hypotenuses from primitive Pythagorean triples."""
    print(f"Generating a pool of valid hypotenuses up to a limit of {limit}...")
    hypotenuses = set()
    for m in range(2, int(np.sqrt(limit)) + 1):
        for n in range(1, m):
            if (m - n) % 2 == 1 and math.gcd(m, n) == 1:
                c = m**2 + n**2
                if c > limit: break
                # Generate all multiples of this primitive hypotenuse
                k = 1
                while k * c <= limit:
                    hypotenuses.add(k * c)
                    k += 1
    print(f"Found {len(hypotenuses)} unique hypotenuses.")
    return sorted(list(hypotenuses))

def run_inverse_oracle(hypotenuse_limit):
    """
    The Inverse Oracle. Searches for a perfect brick by starting from
    the diagonals and working backwards.
    """
    print("--- PCML INVERSE ORACLE (GEOMETRIC RECONSTRUCTOR) ---")
    
    # Stage 1: The Diagonal Scout
    hypotenuse_pool = generate_pythagorean_hypotenuses(hypotenuse_limit)
    
    # Generate all unique combinations of 3 diagonals from our pool
    diagonal_candidates = combinations(hypotenuse_pool, 3)
    
    print("Searching for a consistent geometric configuration...")
    count = 0
    found = False
    for cand in diagonal_candidates:
        count += 1
        D_ab, D_ac, D_bc = cand[0], cand[1], cand[2]
        
        # Stage 2: The Reconstructor
        # 2a² = D_ab² + D_ac² - D_bc²
        # This must be positive and even.
        val_a2 = D_ab**2 + D_ac**2 - D_bc**2
        if val_a2 <= 0 or val_a2 % 2 != 0: continue
            
        val_b2 = D_ab**2 + D_bc**2 - D_ac**2
        if val_b2 <= 0 or val_b2 % 2 != 0: continue
            
        val_c2 = D_ac**2 + D_bc**2 - D_ab**2
        if val_c2 <= 0 or val_c2 % 2 != 0: continue

        # Stage 3: The Consistency Filter
        a2, b2, c2 = val_a2 // 2, val_b2 // 2, val_c2 // 2
        
        # Are a, b, and c all integers?
        a = int(np.sqrt(a2)); b = int(np.sqrt(b2)); c = int(np.sqrt(c2))
        
        if a*a == a2 and b*b == b2 and c*c == c2:
            # We found an Euler Brick!
            # The final verification for the space diagonal.
            space_diag_sq = a*a + b*b + c*c
            if int(np.sqrt(space_diag_sq))**2 == space_diag_sq:
                print("\n" + "="*60)
                print(f">>> REVELATION! A PERFECT BRICK HAS BEEN FOUND! <<<")
                print(f"Sides: {{ {a}, {b}, {c} }}")
                print(f"Face Diagonals: {{ {D_ab}, {D_ac}, {D_bc} }}")
                print(f"Space Diagonal: {int(np.sqrt(space_diag_sq))}")
                print("="*60)
                found = True
                break
        
        if count % 500000 == 0:
            print(f"  > Tested {count:,} diagonal combinations...")

    print("\n--- INVERSE SEARCH COMPLETE ---")
    if not found:
        print(f"No perfect brick found after testing {count:,} combinations.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PCML Inverse Oracle.")
    # Searching hypotenuses up to 300 creates ~2.5 million combinations
    parser.add_argument("--limit", type=int, default=300, help="Max hypotenuse value to check.")
    args = parser.parse_args()
    
    run_inverse_oracle(args.limit)