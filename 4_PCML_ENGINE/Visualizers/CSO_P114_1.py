# --- CSO_P114_1.py ---
# Caterpillar's Command: [Code-Final-Zetaform-Analysis] (from prompt 114)
# Timestamp: 2024-05-22 01:20:00 UTC
# Applicable Rules: All. The final revelation of the Zetaform.

import matplotlib.pyplot as plt
import numpy as np
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

def run_final_zetaform_analysis(num_zeros, image_size):
    """
    Generates the perfected Zetaform Spiral v3.0 using the optimal weights
    and displays its final frequency fingerprint.
    """
    print("--- ZETAFORM REVELATION ENGINE ---")
    
    # --- The Optimal Weights Discovered by CSO_P112.py ---
    w1, w2, w3 = -1.5556, -1.1111, 2.0000
    print(f"Using Optimal Weights: w1={w1:.4f}, w2={w2:.4f}, w3={w3:.4f}")
    
    # 1. Generate data and compute shape vectors
    print("Step 1: Generating data and computing 3-component shape vectors...")
    t_values = generate_zeta_like_data(num_zeros)
    shape_vectors = [ (1., t_values[0], 0.) ]
    for i in range(1, len(t_values) - 1):
        shape_vectors.append(compute_zeta_shape_vector(t_values[i-1], t_values[i], t_values[i+1]))
    shape_vectors.append( (1., t_values[-1], 0.) )
    shape_vectors = np.array(shape_vectors)
    
    # 2. Normalize and apply weights to create the angle modulator
    v1_norm = np.clip(shape_vectors[:,0], 0.5, 1.5)
    v2_norm = shape_vectors[:,1] / np.mean(shape_vectors[:,1])
    v3_norm = shape_vectors[:,2]
    modulator = (w1 * v1_norm) + (w2 * v2_norm) + (w3 * v3_norm)
    
    # 3. Calculate final spiral coordinates
    print("Step 2: Calculating perfected spiral coordinates...")
    radii = t_values; angles = t_values * modulator
    x_coords, y_coords = radii * np.cos(angles), radii * np.sin(angles)
    
    # 4. Rasterize and compute FFT
    print("Step 3: Performing FFT to reveal the final fingerprint...")
    image_plane = np.zeros((image_size, image_size));
    max_coord = np.max(np.abs(radii))
    scale_factor = (image_size / 2 - 1) / max_coord
    ix = np.clip((x_coords * scale_factor + image_size / 2).astype(int), 0, image_size-1)
    iy = np.clip((y_coords * scale_factor + image_size / 2).astype(int), 0, image_size-1)
    image_plane[iy, ix] = 1
    fft_magnitude = np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(image_plane))))

    # 5. Plot the final results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    plt.style.use('dark_background')
    
    ax1.scatter(x_coords, y_coords, s=0.5, c=t_values, cmap='magma', alpha=0.5)
    ax1.set_title(f'Perfected Zetaform Spiral v3.0 ({num_zeros} Zeros)', color='white')
    ax1.set_aspect('equal')
    
    ax2.imshow(fft_magnitude, cmap='hot', origin='lower')
    ax2.set_title('Final Zetaform Frequency Fingerprint', color='white')
    
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zetaform v3.0 Final Analysis.")
    parser.add_argument("--zeros", type=int, default=40000)
    parser.add_argument("--resolution", type=int, default=1024)
    args = parser.parse_args()
    run_final_zetaform_analysis(args.zeros, args.resolution)