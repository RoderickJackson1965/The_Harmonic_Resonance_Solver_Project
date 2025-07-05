# --- CSO_P66.py ---
# Caterpillar's Command: Refine-and-Document (High-Precision Kappa Search)
# Timestamp: 2024-05-21 20:25:00 UTC
# Applicable Rules: All. A high-precision tool for our core constant.

import numpy as np
import time
import argparse

# (generate_primes and calculate_symmetry_score functions are identical to CSO_P59.py, included for monolithic integrity)
def generate_primes(n):
    sieve = np.ones(n // 2, dtype=np.bool_)
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i // 2 - 1]:
            sieve[i*i // 2 - 1::i] = False
    return [2] + [2 * i + 3 for i, v in enumerate(sieve) if v]

def calculate_symmetry_score(fft_magnitude):
    image_size = fft_magnitude.shape[0]
    center = image_size // 2
    mask = np.zeros((image_size, image_size), dtype=bool)
    mask[center-1:center+2, :] = True; mask[:, center-1:center+2] = True
    diag1_indices = np.arange(image_size); diag2_indices = diag1_indices[::-1]
    mask[diag1_indices, diag1_indices] = True; mask[diag1_indices[:-1], diag1_indices[1:]] = True; mask[diag1_indices[1:], diag1_indices[:-1]] = True
    mask[diag1_indices, diag2_indices] = True; mask[diag1_indices[:-1], diag2_indices[1:]] = True; mask[diag1_indices[1:], diag2_indices[:-1]] = True
    scaffold_energy = np.sum(fft_magnitude[mask])
    total_energy = np.sum(fft_magnitude)
    return scaffold_energy / total_energy if total_energy > 0 else 0

def run_kappa_optimizer(num_primes, image_size, search_steps):
    print("--- HIGH-PRECISION KAPPA OPTIMIZER STARTED ---")
    print(f"Parameters: Primes={num_primes}, Resolution={image_size}, Grid Steps={search_steps}")
    print(f"Total iterations: {search_steps*search_steps}. This will take a significant amount of time.")
    
    primes = np.array(generate_primes(int(num_primes * 1.5 * np.log(num_primes)))[:num_primes])
    
    # --- The Refined Search Box ---
    # Centered on our previous best guess (1.70, -0.0064)
    a_range = np.linspace(1.695, 1.705, search_steps)
    b_range = np.linspace(-0.01, 0.0, search_steps)
    # ----------------------------
    
    best_kappa = None; max_score = -1; start_time = time.time()
    total_iterations = search_steps * search_steps; count = 0
    
    for a in a_range:
        for b in b_range:
            count += 1
            if count % 25 == 0 or count == 1: print(f"  > Progress: {count}/{total_iterations}...")

            current_kappa = a + 1j * b
            rescaled_primes = primes / current_kappa
            radii, thetas = np.abs(rescaled_primes), np.angle(rescaled_primes)
            x_coords, y_coords = radii * np.cos(thetas), radii * np.sin(thetas)
            
            image_plane = np.zeros((image_size, image_size))
            max_coord = np.max(np.abs(np.concatenate([x_coords, y_coords])))
            if max_coord == 0: continue
            scale_factor = (image_size / 2 - 1) / max_coord
            ix = np.clip((x_coords * scale_factor + image_size / 2).astype(int), 0, image_size-1)
            iy = np.clip((y_coords * scale_factor + image_size / 2).astype(int), 0, image_size-1)
            image_plane[iy, ix] = 1
            
            fft_magnitude = np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(image_plane))))
            score = calculate_symmetry_score(fft_magnitude)
            
            if score > max_score:
                max_score = score
                best_kappa = current_kappa
    
    end_time = time.time()
    print("\n--- REFINED SEARCH COMPLETE ---")
    print(f"Total search time: {end_time - start_time:.2f} seconds.")
    if best_kappa:
        print(f"Optimal Kappa (κ_refined) Found: {best_kappa.real:.8f} + {best_kappa.imag:.8f}i")
        print(f"Maximum Symmetry Score: {max_score:.6f}")
    else: print("Search did not yield a result.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="High-Precision Kappa Optimizer for Cso Hypothesis.")
    parser.add_argument("--primes", type=int, default=50000, help="Number of primes to use.")
    parser.add_argument("--resolution", type=int, default=512, help="FFT image resolution.")
    parser.add_argument("--steps", type=int, default=50, help="Number of grid steps for the search (e.g., 50 for a 50x50 grid).")
    args = parser.parse_args()
    run_kappa_optimizer(args.primes, args.resolution, args.steps)