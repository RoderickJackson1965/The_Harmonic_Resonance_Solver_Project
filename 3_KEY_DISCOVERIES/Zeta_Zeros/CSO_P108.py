# --- CSO_P108.py ---
# Caterpillar's Command: [Code-Resonant-System-V2] (from prompt 107)
# Timestamp: 2024-05-22 00:45:00 UTC
# Applicable Rules: All. A corrected simulator using the Tangent Flow Process.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import argparse

def run_true_resonance_simulation(shape, steps, focal_distance):
    """
    Simulates a Resonant System (Circle or Ellipse) and generates its
    True Chronospectrum using the Tangent Flow Process.
    """
    print(f"--- TRUE RESONANCE SIMULATOR ({shape.upper()}) ---")
    
    # --- Define Geometry ---
    if shape == 'circle':
        a = 1.0; b = 1.0 # Semi-major and semi-minor axes
    else: # ellipse
        c = focal_distance
        a = c * 1.5; b = np.sqrt(a**2 - c**2)
    print(f"Parameters: a={a:.2f}, b={b:.2f}")

    # Generate the path points
    theta_p = np.linspace(0, 2 * np.pi, steps)
    path_points = np.array([a * np.cos(theta_p), b * np.sin(theta_p)]).T
    
    # Calculate the velocity vectors (the Tangent Flow)
    velocity_vectors = np.diff(path_points, axis=0, append=[path_points[1]]) # Approximate derivative
    
    # Calculate the angles for position and velocity
    position_angles = np.arctan2(path_points[:, 1], path_points[:, 0])
    velocity_angles = np.arctan2(velocity_vectors[:, 1], velocity_vectors[:, 0])

    # Find moments of True Tangent Resonance
    # Where the angle of position is close to the angle of motion
    # We normalize to [0, 2pi) and check for closeness, wrapping around the circle
    diff = np.abs(position_angles - velocity_angles)
    resonance_indices = np.where(np.min([diff, 2*np.pi - diff], axis=0) < 0.01)[0]
    chronospectrum = theta_p[resonance_indices]

    # --- Visualization ---
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.style.use('dark_background')
    ax.set_aspect('equal')
    ax.set_title(f"True Tangent Resonances of a {shape.upper()}", color='white')
    ax.grid(color='gray', linestyle='--', alpha=0.3)
    
    # Plot the path and the resonance points
    ax.plot(path_points[:, 0], path_points[:, 1], '-', color='cyan', lw=1, alpha=0.5)
    ax.scatter(path_points[resonance_indices, 0], path_points[resonance_indices, 1],
               s=150, c='yellow', marker='*', zorder=10)
    plt.show()
    
    # --- Reporting ---
    print("\n--- SIMULATION COMPLETE ---")
    print(f"Generated True Chronospectrum with {len(chronospectrum)} resonance points.")
    print("------------------------------------------")
    # Convert radians to degrees for easier interpretation
    for i, angle in enumerate(chronospectrum):
        print(f"  Resonance {i+1}: θ_p ≈ {np.rad2deg(angle):.2f}°")
    print("------------------------------------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="True Resonance Simulator.")
    parser.add_argument("--shape", type=str, default="ellipse", choices=["circle", "ellipse"])
    args = parser.parse_args()
    
    run_true_resonance_simulation(shape=args.shape, steps=2000, focal_distance=0.8)