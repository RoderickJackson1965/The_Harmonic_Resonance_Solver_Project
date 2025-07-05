# --- CSO_P108_1.py ---
# Caterpillar's Command: [Code-Zeta-Chronospectrum] (from prompt 108)
# Timestamp: 2024-05-22 00:45:00 UTC
# Applicable Rules: All. A Chronospectroscopy analysis of the Zetaform Spiral.

import numpy as np
import matplotlib.pyplot as plt
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

def run_zeta_chronospectroscopy(num_zeros, pacer_speed):
    """
    Generates the Zetaform Spiral v2.0 and analyzes it via Chronospectroscopy.
    """
    print("--- ZETAFORM CHRONOSPECTROSCOPY ENGINE ---")
    
    # 1. Generate the Zetaform Spiral's underlying data
    print("Step 1: Generating Zetaform data...")
    t_values = generate_zeta_like_data(num_zeros)
    shape_hashes = [1.0]
    for i in range(1, len(t_values) - 1):
        shape_hashes.append(compute_zeta_shape_hash(t_values[i-1], t_values[i], t_values[i+1]))
    shape_hashes.append(1.0)
    shape_hashes = np.clip(np.array(shape_hashes), 0.5, 1.5)
    
    # 2. Run the "race" to find Tangent Resonances
    print("Step 2: Searching for Tangent Resonances...")
    chronospectrum = []
    # The process "angle" is the index of the Zeta zero
    for n in range(num_zeros):
        if n == 0: continue
        
        # Calculate the system's angular state
        # θ_psm = t_n * v_ζ(t_n)
        system_psm_angle = t_values[n] * shape_hashes[n]
        system_tan = np.tan(system_psm_angle)
        
        # The Pacer moves at a constant angular velocity
        pacer_angle = n * pacer_speed
        pacer_tan = np.tan(pacer_angle)
        
        if np.isclose(system_tan, pacer_tan, atol=0.05):
            chronospectrum.append(n) # Record the zero index 'n'
            
    print(f"\nFound {len(chronospectrum)} resonance points in the Chronospectrum.")

    # 3. Analyze and visualize the Chronospectrum
    if len(chronospectrum) < 2:
        print("Not enough points to analyze spacing.")
        return
        
    spacings = np.diff(chronospectrum)
    avg_spacing = np.mean(spacings)
    std_dev_spacing = np.std(spacings)
    print("------------------------------------------")
    print(f"Average spacing between resonances: {avg_spacing:.4f} (zero indices)")
    print(f"Standard Deviation of spacing: {std_dev_spacing:.4f}")
    print(f"Normalized Error (std_dev/avg): {std_dev_spacing/avg_spacing:.4f}")
    print("------------------------------------------")
    
    fig, ax = plt.subplots(figsize=(16, 6))
    plt.style.use('dark_background')
    ax.eventplot(chronospectrum, orientation='horizontal', colors='cyan')
    ax.set_title('Chronospectrum of the Zetaform Spiral v2.0', color='white')
    ax.set_xlabel('Zeta Zero Index (n)', color='white')
    ax.set_yticks([])
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zetaform Chronospectroscopy.")
    parser.add_argument("--zeros", type=int, default=50000)
    parser.add_argument("--pacer_speed", type=float, default=0.1)
    args = parser.parse_args()
    run_zeta_chronospectroscopy(args.zeros, args.pacer_speed)