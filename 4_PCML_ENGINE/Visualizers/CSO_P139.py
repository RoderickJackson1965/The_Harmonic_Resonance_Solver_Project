# --- CSO_P139.py ---
# Caterpillar's Command: The Harmonizer - A Deterministic Funnel
# Timestamp: 2024-05-22 03:05:00 UTC
# Applicable Rules: All. The final evolution of the PCML Oracle.

import numpy as np
import argparse
import time

def get_entropy_score(a, b, c):
    """The Judge: Returns the number of non-square diagonals."""
    if a<=0 or b<=0 or c<=0: return 4
    T1 = a*a + b*b; T2 = a*a + c*c; T3 = b*b + c*c; T4 = T1 + c*c
    d1 = 0 if int(np.sqrt(T1))**2 == T1 else 1; d2 = 0 if int(np.sqrt(T2))**2 == T2 else 1
    d3 = 0 if int(np.sqrt(T3))**2 == T3 else 1; d4 = 0 if int(np.sqrt(T4))**2 == T4 else 1
    return float(d1 + d2 + d3 + d4)

def run_harmonizer(a, b, c, iterations, learning_rate):
    """
    The Harmonizer Engine. Takes a single brick and attempts to guide it
    to a zero-entropy state using a harmonic force gradient.
    """
    print("--- PCML HARMONIZER v1.0 ---")
    
    brick = np.array([a, b, c], dtype=float)
    
    print(f"Harmonizing initial brick: {tuple(int(x) for x in brick)}")
    print(f"Iterations: {iterations}, Learning Rate: {learning_rate}")
    
    start_time = time.time()
    for i in range(iterations):
        current_entropy = get_entropy_score(*brick)
        if current_entropy == 0:
            print(f"\n>>> REVELATION! ZERO ENTROPY STATE ACHIEVED AT ITERATION {i+1}! <<<")
            break
        
        a, b, c = brick
        
        # A. Calculate Errors
        T1 = a*a+b*b; S1 = round(np.sqrt(T1))**2; E1 = T1-S1
        T2 = a*a+c*c; S2 = round(np.sqrt(T2))**2; E2 = T2-S2
        T3 = b*b+c*c; S3 = round(np.sqrt(T3))**2; E3 = T3-S3
        T4 = a*a+b*b+c*c; S4 = round(np.sqrt(T4))**2; E4 = T4-S4
        
        # C. Calculate Total Harmonic Force
        # Normalizing factor to keep numbers from exploding
        norm = max(a,b,c)**2
        force_a = (E1 * 2*a + E2 * 2*a + E4 * 2*a) / norm
        force_b = (E1 * 2*b + E3 * 2*b + E4 * 2*b) / norm
        force_c = (E2 * 2*c + E3 * 2*c + E4 * 2*c) / norm
        
        # D. Apply the Nudge
        brick[0] -= learning_rate * force_a
        brick[1] -= learning_rate * force_b
        brick[2] -= learning_rate * force_c
        
        # E. Quantize to nearest valid integers (keep original parity)
        for j in range(3):
            is_odd = int(brick[j]) % 2
            brick[j] = round(brick[j])
            if brick[j] % 2 != is_odd:
                brick[j] += 1
        
        if (i + 1) % 100 == 0:
            print(f"  > Iter {i+1}: Current State {tuple(int(x) for x in brick)} | Entropy: {get_entropy_score(*brick)}")
            
    end_time = time.time()
    final_entropy = get_entropy_score(*brick)
    
    print("\n--- HARMONIZATION COMPLETE ---")
    print(f"Total time: {end_time - start_time:.2f} seconds.")
    if final_entropy == 0:
        print(f">>> PERFECT BRICK FOUND: {tuple(int(x) for x in brick)} <<<")
    else:
        print(f"Process concluded. Best state found: {tuple(int(x) for x in brick)}")
        print(f"Final System Entropy: {final_entropy}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PCML Harmonizer for the Integer Brick Problem.")
    parser.add_argument("a", type=int, help="Starting side a.")
    parser.add_argument("b", type=int, help="Starting side b.")
    parser.add_argument("c", type=int, help="Starting side c.")
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--lr", type=float, default=0.01, help="Learning Rate.")
    args = parser.parse_args()
    
    run_harmonizer(args.a, args.b, args.c, args.iterations, args.lr)