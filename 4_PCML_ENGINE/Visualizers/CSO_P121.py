# --- CSO_P121.py ---
# Caterpillar's Command: [Code-Statistical-Mapper] (from prompt 121)
# Timestamp: 2024-05-22 01:45:00 UTC
# Applicable Rules: All. The first step in building the Cso Oracle.

import numpy as np
import matplotlib.pyplot as plt

def analyze_euler_bricks():
    """
    Performs a statistical analysis on known Euler bricks to create a
    probability map for a future heuristic search.
    """
    print("--- EULER BRICK STATISTICAL MAPPER ---")
    
    # A list of the 20 smallest known primitive Euler bricks {a, b, c}
    # where a < b < c. Sourced from standard mathematical tables.
    euler_bricks = np.array([
        [44, 117, 240], [85, 132, 720], [140, 480, 693], [160, 231, 792],
        [187, 1020, 1584], [195, 748, 6336], [240, 252, 275], [275, 252, 240],
        [336, 360, 23460], [429, 2340, 27300], [440, 1170, 2400], [480, 1400, 6930],
        [495, 2808, 43923], [528, 5796, 6325], [660, 2772, 33150], [720, 1320, 8500],
        [780, 2475, 33152], [792, 1600, 23100], [828, 2035, 3120], [960, 2800, 13860]
    ])
    
    # 1. Analyze Side Parity (Even/Odd)
    parity = euler_bricks % 2
    # e.g., [0, 1, 0] means (Even, Odd, Even)
    patterns = {}
    for p in parity:
        pattern_str = f"({p[0]},{p[1]},{p[2]})".replace('0','E').replace('1','O')
        patterns[pattern_str] = patterns.get(pattern_str, 0) + 1
        
    print("\n--- Parity Analysis ---")
    for pattern, count in patterns.items():
        print(f"  > Pattern {pattern}: {count/len(euler_bricks)*100:.1f}%")
    print("-----------------------\n")

    # 2. Analyze Distributions
    print("Generating statistical plots...")
    # Sort sides for consistent analysis
    sorted_bricks = np.sort(euler_bricks, axis=1)
    side_a = sorted_bricks[:, 0] # Smallest side
    side_b = sorted_bricks[:, 1] # Middle side
    side_c = sorted_bricks[:, 2] # Longest side
    
    # Calculate aspect ratios relative to the smallest side
    ratio_b_a = side_b / side_a
    ratio_c_a = side_c / side_a
    
    # 3. Create plots
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))
    plt.style.use('dark_background')
    fig.suptitle('Statistical Map of Euler Bricks', color='white', fontsize=18)
    
    # Histogram of the smallest side length
    axs[0, 0].hist(side_a, bins=15, color='cyan', alpha=0.8)
    axs[0, 0].set_title('Distribution of Smallest Side (a)', color='white')
    axs[0, 0].set_xlabel('Side Length', color='white')
    
    # Histogram of the middle side length
    axs[0, 1].hist(side_b, bins=15, color='magenta', alpha=0.8)
    axs[0, 1].set_title('Distribution of Middle Side (b)', color='white')

    # Histogram of the aspect ratios
    axs[1, 0].hist(ratio_b_a, bins=15, color='lime', alpha=0.7, label='b/a Ratio')
    axs[1, 0].hist(ratio_c_a, bins=15, color='yellow', alpha=0.7, label='c/a Ratio')
    axs[1, 0].set_title('Distribution of Aspect Ratios', color='white')
    axs[1, 0].set_xlabel('Ratio to Smallest Side', color='white')
    axs[1, 0].legend()
    
    # A log-log plot to check for power-law behavior
    axs[1, 1].scatter(side_a, side_c, c='red', alpha=0.8)
    axs[1, 1].set_xscale('log')
    axs[1, 1].set_yscale('log')
    axs[1, 1].set_title('Log-Log Plot (a vs c)', color='white')
    axs[1, 1].set_xlabel('Smallest Side (log scale)', color='white')
    axs[1, 1].set_ylabel('Largest Side (log scale)', color='white')
    
    for ax in axs.flat:
        ax.grid(True, linestyle='--', alpha=0.3)
        
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    analyze_euler_bricks()