# --- CSO_P118.py (Corrected) ---
# Caterpillar's Command: Implementing the Half-Plane Analysis method.
# Timestamp: 2024-05-22 01:55:00 UTC
# Applicable Rules: All. A more intelligent measurement tool.

import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
import argparse

# (generate_zeta_like_data and compute_zeta_shape_vector are unchanged)
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

def run_plateau_analyzer_v2(num_zeros, image_size, threshold_ratio):
    print("--- ZETA LOBE PLATEAU ANALYZER v2.0 (HALF-PLANE) ---")
    
    w1, w2, w3 = -1.5556, -1.1111, 2.0000
    t_values = generate_zeta_like_data(num_zeros)
    shape_vectors = [ (1., t_values[0], 0.) ]
    for i in range(1, len(t_values) - 1):
        shape_vectors.append(compute_zeta_shape_vector(t_values[i-1], t_values[i], t_values[i+1]))
    shape_vectors.append( (1., t_values[-1], 0.) )
    shape_vectors = np.array(shape_vectors)
    
    v1_norm = np.clip(shape_vectors[:,0], 0.5, 1.5)
    v2_norm = shape_vectors[:,1] / np.mean(shape_vectors[:,1])
    v3_norm = shape_vectors[:,2]
    modulator = (w1 * v1_norm) + (w2 * v2_norm) + (w3 * v3_norm)
    
    radii = t_values; angles = t_values * modulator
    x_coords, y_coords = radii * np.cos(angles), radii * np.sin(angles)
    
    image_plane = np.zeros((image_size, image_size));
    max_coord = np.max(np.abs(radii))
    scale_factor = (image_size / 2 - 1) / max_coord
    ix = np.clip((x_coords * scale_factor + image_size / 2).astype(int), 0, image_size-1)
    iy = np.clip((y_coords * scale_factor + image_size / 2).astype(int), 0, image_size-1)
    image_plane[iy, ix] = 1
    
    fft_magnitude = np.log1p(np.abs(np.fft.fftshift(np.fft.fft2(image_plane))))
    
    # --- THE NEW, CORRECTED HALF-PLANE ANALYSIS ---
    center_pixel = image_size // 2
    max_intensity = np.max(fft_magnitude)
    threshold_value = max_intensity * threshold_ratio
    plateau_mask = fft_magnitude > threshold_value
    
    # Create a mask for the upper half of the image
    half_plane_mask = np.zeros_like(plateau_mask)
    half_plane_mask[center_pixel:, :] = True
    
    # Only consider the plateau in the upper half-plane
    final_mask = plateau_mask & half_plane_mask
    
    com = ndimage.center_of_mass(fft_magnitude, labels=final_mask)
    # --- END OF NEW LOGIC ---

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.style.use('dark_background')
    ax.imshow(fft_magnitude, cmap='hot', origin='lower')
    
    print("\n--- MEASUREMENT COMPLETE ---")
    if not np.isnan(com).any():
        peak_y, peak_x = com
        r_zeta_lobe = np.hypot(peak_x - center_pixel, peak_y - center_pixel)
        theta_zeta_lobe = np.rad2deg(np.arctan2(peak_y - center_pixel, peak_x - center_pixel))
        ax.scatter([peak_x], [peak_y], s=200, c='lime', marker='x', lw=2)
        print(f"Center of Mass of Plateau (y, x): ({peak_y:.2f}, {peak_x:.2f})")
        print("-----------------------------------------------------")
        print(f"Zeta Lobe Frequency (r_ζ_lobe) ≈ {r_zeta_lobe:.4f}")
        print(f"Zeta Lobe Angle (θ_ζ_lobe)   ≈ {theta_zeta_lobe:.4f}°")
        print("-----------------------------------------------------")
    else: print("Could not find a significant plateau.")
    
    ax.set_title('Zetaform Fingerprint with Correctly Measured Plateau', color='white')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zeta Lobe Plateau Analyzer v2.0.")
    parser.add_argument("--zeros", type=int, default=50000)
    parser.add_argument("--resolution", type=int, default=1024)
    parser.add_argument("--threshold", type=float, default=0.90)
    args = parser.parse_args()
    run_plateau_analyzer_v2(args.zeros, args.resolution, args.threshold)