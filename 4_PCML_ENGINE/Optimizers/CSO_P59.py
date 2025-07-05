# --- CSO_P59.py (Restored) ---
# Caterpillar's Command: Restoration of a corrupt tool.
# Timestamp: 2024-05-21 20:20:00 UTC
# Applicable Rules: 2, 4, 5, 6, 11, 12

import numpy as np
import time
import argparse

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
    mask[center-1:center+2, :] = True
    mask[:, center-1:center+2] = True
    diag1_indices = np.arange(image_size)
    diag2_indices = diag1_indices[::-1]
    mask[diag1_indices, diag1_indices] = True
    mask[diag1_indices[:-1], diag1_indices[1:]] = True
    mask[diag1_indices[1:], diag1_indices[:-1]] = True
    mask[diag1_indices, diag2_indices] = True
    mask[diag1_indices[:-1], diag2_indices[1:]] = True
    mask[diag1_indices[1:], diag2_indices[:-1]] = True
    scaffold_energy = np.sum(fft_magnitude[mask])
    total_energy = np.sum(fft_magnitude)
    return scaffold_energy / total_energy if total_energy > 0 else 0

def run_kappa_optimizer(num_primes, image_size, search_steps):
    print("--- KAPPA OPTIMIZER ENGINE STARTED ---")
    print(f"Parameters: Primes={num_primes}, Resolution={image_size}, Grid Steps={search_steps}")
    print(f"Total iterations: {search_steps*search_steps}")
    
    primes = np.array(generate_primes(int(num_primes * 1.5 * np.log(num_primes)))[:num_primes])
    
    a_range = np.linspace(1.7, 1.75, search_steps)
    b_range = np.linspace(-0.05, 0.05, search_steps)
    
    best_kappa = None
    max_score = -1
    start_time = time.time()
    total_iterations = search_steps * search_steps
    count = 0
    
    for a in a_range:
        for b in b_range:
            count += 1
            if count % 10 == 0 or count == 1:
                print(f"  > Progress: {count}/{total_iterations} iterations...")

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
    print("\n--- SEARCH COMPLETE ---")
    print(f"Total search time: {end_time - start_time:.2f} seconds.")
    if best_kappa:
        print(f"Optimal Kappa (κ) Found: {best_kappa.real:.6f} + {best_kappa.imag:.6f}i")
        print(f"Maximum Symmetry Score: {max_score:.6f}")
    else:
        print("Search did not yield a result.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kappa Optimizer for Cso Hypothesis.")
    parser.add_argument("--primes", type=int, default=10000, help="Number of primes to use.")
    parser.add_argument("--resolution", type=int, default=256, help="FFT image resolution (a power of 2).")
    parser.add_argument("--steps", type=int, default=20, help="Number of grid steps for the search.")
    
    args = parser.parse_args()
    
    run_kappa_optimizer(args.primes, args.resolution, args.steps)