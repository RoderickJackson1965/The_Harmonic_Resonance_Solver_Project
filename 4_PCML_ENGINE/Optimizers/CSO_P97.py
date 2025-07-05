# --- CSO_P97.py (Corrected) ---
# Caterpillar's Command: Correction of a typo in the command-line parser.
# Timestamp: 2024-05-21 23:25:00 UTC
# Applicable Rules: All. A new, mathematically sound search engine.

import numpy as np
import time
import argparse

def generate_zeta_like_data(n):
    t_values = []; current_t = 14.134725
    while len(t_values) < n:
        t_values.append(current_t); gap = (2 * np.pi) / np.log(current_t)
        current_t += gap * (1 + (np.random.rand() - 0.5) * 0.1)
    return np.array(t_values)

def compute_zeta_shape_hash(t_prev, t_curr, t_next):
    try:
        g_in = t_curr - t_prev; g_out = t_next - t_curr
        if g_in <= 1e-9 or g_out <= 1e-9: return 1.0
        return np.log(g_out) / np.log(g_in)
    except (ValueError, ZeroDivisionError): return 1.0

def calculate_zeta_symmetry_score(fft_magnitude):
    image_size = fft_magnitude.shape[0]; center = image_size // 2
    mask = np.zeros((image_size, image_size), dtype=bool)
    mask[center-1:center+2, :] = True
    scaffold_energy = np.sum(fft_magnitude[mask]); total_energy = np.sum(fft_magnitude)
    return scaffold_energy / total_energy if total_energy > 0 else 0

def run_zeta_optimizer_v3(num_zeros, image_size, search_steps, a_min, a_max, b_min, b_max):
    print("--- ZETA OPTIMIZER ENGINE v3.0 (κ_ζ HUNTER) ---")
    print(f"Parameters: Zeros={num_zeros}, Res={image_size}, Steps={search_steps}")
    print(f"Search Box: Real=[{a_min}, {a_max}], Imag=[{b_min}, {b_max}]")
    
    t_values = generate_zeta_like_data(num_zeros)
    shape_hashes = [1.0]
    for i in range(1, len(t_values) - 1):
        shape_hashes.append(compute_zeta_shape_hash(t_values[i-1], t_values[i], t_values[i+1]))
    shape_hashes.append(1.0)
    shape_hashes = np.clip(np.array(shape_hashes), 0.5, 1.5)
    
    base_angles = t_values * shape_hashes
    
    a_range = np.linspace(a_min, a_max, search_steps)
    b_range = np.linspace(b_min, b_max, search_steps)
    
    best_kappa_zeta = None; max_score = -1; start_time = time.time()
    
    for a in a_range:
        for b in b_range:
            current_kappa_zeta = a + 1j * b
            
            kappa_mag = np.abs(current_kappa_zeta)
            kappa_angle = np.angle(current_kappa_zeta)
            if kappa_mag < 1e-9: continue
            
            angles = (base_angles / kappa_mag) - kappa_angle
            
            radii = t_values
            x_coords, y_coords = radii * np.cos(angles), radii * np.sin(angles)
            
            image_plane = np.zeros((image_size, image_size))
            max_coord = np.max(np.abs(radii))
            if max_coord == 0: continue
            scale_factor = (image_size / 2 - 1) / max_coord
            ix = np.clip((x_coords * scale_factor + image_size / 2).astype(int), 0, image_size-1)
            iy = np.clip((y_coords * scale_factor + image_size / 2).astype(int), 0, image_size-1)
            image_plane[iy, ix] = 1
            
            fft_magnitude = np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(image_plane))))
            score = calculate_zeta_symmetry_score(fft_magnitude)
            
            if score > max_score:
                max_score = score
                best_kappa_zeta = current_kappa_zeta

    end_time = time.time()
    print("\n--- ZETA SEARCH COMPLETE ---")
    print(f"Total search time: {end_time - start_time:.2f} seconds.")
    if best_kappa_zeta:
        print(f"Optimal Zeta Impedance (κ_ζ) Found: {best_kappa_zeta.real:.8f} + {best_kappa_zeta.imag:.8f}i")
        print(f"Maximum Symmetry Score: {max_score:.6f}")
    else: print("Search did not yield a result.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zeta Resonance Impedance Optimizer v3.0.")
    parser.add_argument("--zeros", type=int, default=5000)
    parser.add_argument("--resolution", type=int, default=256)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--a_min", type=float, default=1.42)
    parser.add_argument("--a_max", type=float, default=1.44)
    # --- TYPO FIX IS HERE ---
    parser.add_argument("--b_min", type=float, default=-0.13)
    # -----------------------
    parser.add_argument("--b_max", type=float, default=-0.11)
    
    args = parser.parse_args()
    run_zeta_optimizer_v3(args.zeros, args.resolution, args.steps, args.a_min, args.a_max, args.b_min, args.b_max)