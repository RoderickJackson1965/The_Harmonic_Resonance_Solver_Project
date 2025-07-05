# --- CSO_P107.py ---
# Caterpillar's Command: [Code-Lattice-Chronospectrum] (from prompt 107)
# Timestamp: 2024-05-22 00:35:00 UTC
# Applicable Rules: All. A Chronospectroscopy analysis of the Prime Lattice.

import numpy as np
import matplotlib.pyplot as plt
import argparse

def generate_primes(n):
    sieve = np.ones(n // 2, dtype=np.bool_)
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i // 2 - 1]:
            sieve[i*i // 2 - 1::i] = False
    return [2] + [2 * i + 3 for i, v in enumerate(sieve) if v]

def run_lattice_chronospectroscopy(num_primes, pacer_speed):
    """
    Generates the Prime Lattice and analyzes it via Chronospectroscopy.
    """
    print("--- PRIME LATTICE CHRONOSPECTROSCOPY ENGINE ---")
    
    # 1. Generate the Prime Lattice points
    kappa_refined = 1.69500000 - 0.00653061j
    print(f"Generating Prime Lattice with κ_refined = {kappa_refined:.8f}")
    primes = np.array(generate_primes(int(num_primes * 1.5 * np.log(num_primes)))[:num_primes])
    lattice_points = primes / kappa_refined
    
    # 2. Run the "race" to find Tangent Resonances
    print("Searching for Tangent Resonances...")
    chronospectrum = []
    # The process "angle" here is just the index of the prime
    for n, point in enumerate(lattice_points):
        if n == 0: continue
            
        system_angle = np.angle(point) # The angle of the n-th point on the lattice
        pacer_angle = n * pacer_speed  # The Pacer moves at a constant angular velocity
        
        # We check the tangents for resonance
        system_tan = np.tan(system_angle)
        pacer_tan = np.tan(pacer_angle)
        
        if np.isclose(system_tan, pacer_tan, atol=0.01):
            chronospectrum.append(n) # Record the prime index 'n'
            
    print(f"\nFound {len(chronospectrum)} resonance points in the Chronospectrum.")

    # 3. Analyze and visualize the Chronospectrum
    if len(chronospectrum) < 2:
        print("Not enough points to analyze spacing.")
        return
        
    spacings = np.diff(chronospectrum)
    avg_spacing = np.mean(spacings)
    print("------------------------------------------")
    print(f"Average spacing between resonances: {avg_spacing:.4f} (prime indices)")
    print("------------------------------------------")
    
    fig, ax = plt.subplots(figsize=(16, 6))
    plt.style.use('dark_background')
    ax.eventplot(chronospectrum, orientation='horizontal', colors='lime')
    ax.set_title('Chronospectrum of the Prime Lattice', color='white')
    ax.set_xlabel('Prime Index (n)', color='white')
    ax.set_yticks([])
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prime Lattice Chronospectroscopy.")
    parser.add_argument("--primes", type=int, default=50000)
    parser.add_argument("--pacer_speed", type=float, default=0.01)
    args = parser.parse_args()
    run_lattice_chronospectroscopy(args.primes, args.pacer_speed)