# --- CSO_P106.py ---
# Caterpillar's Command: [Code-Resonant-Ellipse] (from prompt 106)
# Timestamp: 2024-05-22 00:25:00 UTC
# Applicable Rules: All. A simulation of the de-rigidized ellipse.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import argparse

def run_resonant_ellipse_simulation(steps, pacer_speed, focal_distance):
    """
    Simulates and visualizes a Resonant Ellipse, its Pacer Process,
    and the moments of Tangent Resonance to generate its Chronospectrum.
    """
    print("--- RESONANT ELLIPSE SIMULATOR v1.0 ---")
    
    # --- Define Ellipse Properties based on foci ---
    # Foci are at (-c, 0) and (c, 0)
    c = focal_distance
    # Let's define the sum of distances to be constant, say 2a
    a = c * 1.5 # Semi-major axis (must be > c)
    b = np.sqrt(a**2 - c**2) # Semi-minor axis
    
    print(f"Ellipse Parameters: a={a:.2f}, b={b:.2f}, c={c:.2f}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    plt.style.use('dark_background')
    
    # Setup for ax1 (The Ellipse)
    ax1.set_xlim(-a*1.2, a*1.2); ax1.set_ylim(-a*1.2, a*1.2)
    ax1.set_aspect('equal'); ax1.set_title("Resonant Ellipse System", color='white')
    ax1.grid(color='gray', linestyle='--', alpha=0.3)
    
    # Draw the ellipse path and foci
    ellipse_path = plt.matplotlib.patches.Ellipse((0, 0), 2*a, 2*b, color='cyan', fill=False, linestyle='--')
    ax1.add_artist(ellipse_path)
    ax1.plot([-c, c], [0, 0], 'x', color='red', markersize=10, label='Foci')
    
    # Initialize plot elements
    system_point, = ax1.plot([], [], 'o', markersize=12, color='lime')
    potential_vector, = ax1.plot([], [], '-', lw=2, color='lime')
    pacer_line, = ax1.plot([], [], '-', lw=2, color='magenta', alpha=0.7)
    resonance_flash = ax1.scatter([], [], s=250, facecolors='none', edgecolors='yellow', lw=3)
    
    # Setup for ax2 (The Chronospectrum)
    ax2.set_xlim(0, 2 * np.pi); ax2.set_ylim(0, 1)
    ax2.set_title("Ellipse Chronospectrum", color='white')
    ax2.set_xlabel("Process Angle (θ_p)", color='white'); ax2.set_yticks([])
    
    chronospectrum = []

    def update(frame):
        theta_p = (frame / steps) * 2 * np.pi
        
        # PSM Processes using parametric equations for the ellipse
        x = a * np.cos(theta_p) # ~>h(θ_p)
        y = b * np.sin(theta_p) # ~|v(θ_p)
        
        pacer_angle = theta_p * pacer_speed
        system_angle = np.arctan2(y, x) # The actual angle of the vector
        
        try:
            pacer_state = np.tan(pacer_angle)
            system_angle_state = np.tan(system_angle)
            is_close = np.isclose(pacer_state, system_angle_state, atol=0.05)
        except FloatingPointError: is_close = False

        system_point.set_data([x], [y])
        potential_vector.set_data([0, x], [0, y])
        
        pacer_x = np.cos(np.arctan(pacer_state)) if not np.isinf(pacer_state) else 0
        pacer_y = np.sin(np.arctan(pacer_state)) if not np.isinf(pacer_state) else 1 * np.sign(pacer_state)
        pacer_line.set_data([-pacer_x*a*1.2, pacer_x*a*1.2], [-pacer_y*a*1.2, pacer_y*a*1.2])
        
        if is_close:
            resonance_flash.set_offsets(np.array([[x, y]]))
            if not any(np.isclose(theta_p, val, atol=0.01) for val in chronospectrum):
                chronospectrum.append(theta_p)
                ax2.axvline(theta_p, color='yellow', linestyle='-', alpha=0.5)
        else:
            resonance_flash.set_offsets(np.array([]).reshape(0, 2))
            
        return system_point, potential_vector, pacer_line, resonance_flash

    ani = FuncAnimation(fig, update, frames=steps, interval=20, blit=True, repeat=False)
    plt.show()
    
    print("\n--- SIMULATION COMPLETE ---")
    print(f"Generated Ellipse Chronospectrum with {len(chronospectrum)} resonance points.")
    print("------------------------------------------")
    for i, angle in enumerate(chronospectrum[:10]):
        print(f"  Resonance {i+1}: θ_p ≈ {angle:.4f} radians")
    print("------------------------------------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resonant Ellipse Simulator v1.0")
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--pacer_speed", type=float, default=2.5)
    parser.add_argument("--foci_dist", type=float, default=0.8, help="Distance of foci from center.")
    args = parser.parse_args()
    run_resonant_ellipse_simulation(args.steps, args.pacer_speed, args.foci_dist)