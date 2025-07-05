# --- CSO_P112.py ---
# Caterpillar's Command: [Code-Weight-Optimizer] (from prompt 112)
# Timestamp: 2024-05-22 01:10:00 UTC
# Applicable Rules: All. A heuristic search engine to learn the Zetaform formula.

import matplotlib.pyplot as plt
import numpy as np
import time
import argparse

def generate_zeta_like_data(n):
    t_values = []; current_t = 14.134725
    while len(t_values) < n:
        t_values.append(current_t); gap = (2 * np.pi) / np.log(current_t)
        current_t += gap * (1 + (np.random.rand() - 0.5) * 0.1)
    return np.array(t_values)

def compute_zeta_shape_vector(t_prev, t_curr, t_next):
    try:
        g_in = t_curr - t_prev; g_out = t_next - t_curr
        if g_in <= 1e-9 or g_out <= 1e-9: return (1.0, 1.0, 0.0)
        v1 = np.log(g_out) / np.log(g_in); v2 = (g_in + g_out) / 2
        v3 = np.abs(g_out - g_in) / (g_in + g_out)
        return (v1, v2, v3)
    except (ValueError, ZeroDivisionError): return (1.0, 1.0, 0.0)

def calculate_peak_intensity_score(fft_magnitude):
    """Measures the intensity of the brightest off-center peak."""
    image_size = fft_magnitude.shape[0]; center = image_size // 2
    # Create a mask to block out the central DC component
    fft_magnitude[center-5:center+6, center-5:center+6] = 0
    # The score is simply the value of the brightest remaining pixel
    return np.max(fft_magnitude)

def run_weight_optimizer(num_zeros, image_size, search_steps):
    print("--- ZETAFORM WEIGHT OPTIMIZER v1.0 ---")
    print(f"Parameters: Zeros={num_zeros}, Res={image_size}, Steps={search_steps}")
    print(f"Total iterations: {search_steps**3}. This may take a very long time.")
    
    t_values = generate_zeta_like_data(num_zeros)
    shape_vectors = [ (1., t_values[0], 0.) ]
    for i in range(1, len(t_values) - 1):
        shape_vectors.append(compute_zeta_shape_vector(t_values[i-1], t_values[i], t_values[i+1]))
    shape_vectors.append( (1., t_values[-1], 0.) )
    shape_vectors = np.array(shape_vectors)
    
    v1_norm = np.clip(shape_vectors[:,0], 0.5, 1.5)
    v2_norm = shape_vectors[:,1] / np.mean(shape_vectors[:,1])
    v3_norm = shape_vectors[:,2]
    
    w_range = np.linspace(-2.0, 2.0, search_steps)
    
    best_weights = None; max_score = -1; start_time = time.time()
    count = 0
    
    for w1 in w_range:
        for w2 in w_range:
            for w3 in w_range:
                count += 1
                if count % 25 == 0: print(f"  > Progress: {count}/{search_steps**3}...")
                
                modulator = (w1 * v1_norm) + (w2 * v2_norm) + (w3 * v3_norm)
                angles = t_values * modulator
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
                score = calculate_peak_intensity_score(fft_magnitude)
            
                if score > max_score:
                    max_score = score
                    best_weights = (w1, w2, w3)
                    print(f"  > New best weights found: w1={w1:.3f}, w2={w2:.3f}, w3={w3:.3f} | Score: {score:.4f}")

    end_time = time.time()
    print("\n--- WEIGHT SEARCH COMPLETE ---")
    print(f"Total search time: {end_time - start_time:.2f} seconds.")
    if best_weights:
        w1, w2, w3 = best_weights
        print(f"Optimal Weights Found: w1={w1:.4f}, w2={w2:.4f}, w3={w3:.4f}")
        print(f"Achieved Maximum Peak Intensity Score: {max_score:.4f}")
    else: print("Search did not yield a result.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zetaform Weight Optimizer.")
    parser.add_argument("--zeros", type=int, default=5000)
    parser.add_argument("--resolution", type=int, default=128) # Lower res for speed
    parser.add_argument("--steps", type=int, default=10) # 10x10x10 = 1000 iterations
    args = parser.parse_args()
    run_weight_optimizer(args.zeros, args.resolution, args.steps)