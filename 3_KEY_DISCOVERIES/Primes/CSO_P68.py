# --- CSO_P68.py ---
# Caterpillar's Command: The Final Test with κ_refined
# Timestamp: 2024-05-21 20:35:00 UTC
# Applicable Rules: All. The ultimate test of our refined constant.

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import argparse

def generate_primes(n):
    sieve = np.ones(n // 2, dtype=np.bool_)
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i // 2 - 1]:
            sieve[i*i // 2 - 1::i] = False
    return [2] + [2 * i + 3 for i, v in enumerate(sieve) if v]

def run_final_test(num_primes, num_bins):
    print("--- HIGH-PRECISION LANE ANALYSIS ENGINE ---")
    
    # --- The High-Precision Constant ---
    kappa_refined = 1.69500000 - 0.00653061j 
    print(f"Testing with κ_refined = {kappa_refined:.8f}")
    
    # 1. Generate and transform primes
    print(f"Generating and transforming {num_primes} primes...")
    primes = np.array(generate_primes(int(num_primes * 1.5 * np.log(num_primes)))[:num_primes])
    transformed_points = primes / kappa_refined
    y_coords = transformed_points.imag

    # 2. Create a high-resolution histogram
    print("Creating high-resolution histogram of the Prime Lattice...")
    # Focus on the very narrow central region where lanes are expected
    hist_counts, bin_edges = np.histogram(y_coords, bins=num_bins, range=(-5, 5))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # 3. Find peaks (the lane centers)
    # We set the height dynamically based on the noise floor
    mean_count = np.mean(hist_counts)
    std_count = np.std(hist_counts)
    min_peak_height = mean_count + (2.5 * std_count) # Peaks must be 2.5 std_devs above the mean
    peaks, _ = find_peaks(hist_counts, height=min_peak_height, distance=5)
    lane_centers = bin_centers[peaks]
    
    print(f"\nFound {len(lane_centers)} distinct lattice lanes.")
    
    # 4. Calculate lambda
    if len(lane_centers) > 1:
        lane_spacings = np.diff(np.sort(lane_centers))
        lambda_val = np.mean(lane_spacings)
        lambda_std = np.std(lane_spacings)
        print("------------------------------------------")
        print(f"Fundamental Lane Spacing (λ_p) ≈ {lambda_val:.6f}")
        print(f"Standard Deviation of Spacing: {lambda_std:.6f}")
        print("------------------------------------------")

    # 5. Visualization
    fig, ax = plt.subplots(figsize=(16, 9))
    plt.style.use('dark_background')
    ax.bar(bin_centers, hist_counts, width=(bin_centers[1]-bin_centers[0])*0.9, color='lime')
    
    for center in lane_centers:
        ax.axvline(center, color='red', linestyle='--', alpha=0.8)
        
    ax.set_title('The Prime Lattice (Corrected by High-Precision κ)', color='white')
    ax.set_xlabel('Imaginary Component (Lane Position)', color='white')
    ax.set_ylabel('Frequency (Number of Primes)', color='white')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Final Test of the refined Kappa constant.")
    parser.add_argument("--primes", type=int, default=250000, help="Number of primes to use.")
    parser.add_argument("--bins", type=int, default=4000, help="Number of bins for the histogram.")
    
    args = parser.parse_args()
    
    run_final_test(args.primes, args.bins)