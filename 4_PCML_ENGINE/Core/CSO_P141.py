# --- CSO_P141.py (Corrected) ---
# Caterpillar's Command: Correction of a NameError in the Harmonizer.
# Timestamp: 2024-05-22 03:20:00 UTC
# Applicable Rules: All. The Grand Harmonizer, the synthesis of our work.

import numpy as np
import argparse
import time

def calculate_entropy(a, b, c):
    """S: Correctness Stress"""
    a,b,c = int(a), int(b), int(c)
    if a<=0 or b<=0 or c<=0: return 4.0
    T1 = a*a + b*b; T2 = a*a + c*c; T3 = b*b + c*c; T4 = T1 + c*c
    d1 = 0 if int(np.sqrt(T1))**2 == T1 else 1; d2 = 0 if int(np.sqrt(T2))**2 == T2 else 1
    d3 = 0 if int(np.sqrt(T3))**2 == T3 else 1; d4 = 0 if int(np.sqrt(T4))**2 == T4 else 1
    return float(d1 + d2 + d3 + d4)

def calculate_geometric_disharmony(a, b, c):
    """H_geom: Elegance Stress"""
    a,b,c = float(a), float(b), float(c)
    h_ab = abs(b/a - 1) if a != 0 else float('inf')
    h_ac = abs(c/a - 1) if a != 0 else float('inf')
    h_bc = abs(c/b - 1) if b != 0 else float('inf')
    return h_ab + h_ac + h_bc

def calculate_rhythmic_disharmony(a, b, c):
    """H_rhythm: Zetaform Stress"""
    sides = sorted((a, b, c))
    g_in = sides[1] - sides[0]; g_out = sides[2] - sides[1]
    if g_in <= 1e-9 or g_out <= 1e-9: return 1.0
    return np.abs(g_out - g_in) / (g_in + g_out)

def calculate_unifying_disharmony(a, b, c):
    """H_unify: Universal Stress"""
    kappa_prime_mag = 1.69501254
    r_zeta_lobe = 0.2438
    ideal_shape_hash = r_zeta_lobe / kappa_prime_mag
    actual_shape_hash = (a+b+c) / np.sqrt(a*a+b*b+c*c) if (a*a+b*b+c*c)>0 else 0
    return np.abs(actual_shape_hash - ideal_shape_hash)

def run_grand_harmonizer(a, b, c, iterations, lr, weights):
    print("--- PCML GRAND HARMONIZER v1.1 (Corrected) ---")
    brick = np.array([a, b, c], dtype=float)
    w_S, w_Hg, w_Hr, w_Hu = weights

    print(f"Harmonizing initial brick: {tuple(int(x) for x in brick)}")

    start_time = time.time()
    for i in range(iterations):
        S0 = calculate_entropy(*brick)
        if S0 == 0:
            print(f"\n>>> REVELATION! ZERO ENTROPY STATE ACHIEVED AT ITERATION {i+1}! <<<")
            break

        Hg0 = calculate_geometric_disharmony(*brick)
        Hr0 = calculate_rhythmic_disharmony(*brick)
        Hu0 = calculate_unifying_disharmony(*brick)
        
        # Calculate gradients for all forces on side 'a'
        grad_S_a = calculate_entropy(brick[0]+1, brick[1], brick[2]) - S0
        grad_Hg_a = calculate_geometric_disharmony(brick[0]+1, brick[1], brick[2]) - Hg0
        grad_Hr_a = calculate_rhythmic_disharmony(brick[0]+1, brick[1], brick[2]) - Hr0
        grad_Hu_a = calculate_unifying_disharmony(brick[0]+1, brick[1], brick[2]) - Hu0
        
        # This is a simplified model. A true multi-variate gradient is more complex.
        # For now, we apply a combined force.
        force_a = w_S*grad_S_a + w_Hg*grad_Hg_a + w_Hr*grad_Hr_a + w_Hu*grad_Hu_a
        brick[0] -= lr * force_a
        
        # Repeat for b and c (simplified for this test)
        grad_S_b = calculate_entropy(brick[0], brick[1]+1, brick[2]) - S0
        grad_S_c = calculate_entropy(brick[0], brick[1], brick[2]+1) - S0
        brick[1] -= lr * grad_S_b; brick[2] -= lr * grad_S_c

        brick = np.round(np.abs(brick))
        
        if (i + 1) % 200 == 0:
            # --- TYPO FIX IS HERE ---
            print(f"  > Iter {i+1}: Current State {tuple(int(x) for x in brick)} | Entropy: {calculate_entropy(*brick):.1f}")
            # --- END OF FIX ---
            
    end_time = time.time()
    final_entropy = calculate_entropy(*brick)
    
    print("\n--- HARMONIZATION COMPLETE ---")
    print(f"Total time: {end_time - start_time:.2f} seconds.")
    if final_entropy == 0:
        print(f">>> PERFECT BRICK FOUND: {tuple(int(x) for x in brick)} <<<")
    else:
        print(f"Process concluded. Best state found: {tuple(int(x) for x in brick)}")
        print(f"Final System Entropy: {final_entropy}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PCML Grand Harmonizer.")
    parser.add_argument("a", type=int); parser.add_argument("b", type=int); parser.add_argument("c", type=int)
    parser.add_argument("--iterations", type=int, default=2000)
    parser.add_argument("--lr", type=float, default=0.05)
    args = parser.parse_args()
    
    force_weights = [1.0, 0.01, 0.01, 0.005]
    run_grand_harmonizer(args.a, args.b, args.c, args.iterations, args.lr, force_weights)