# --- CSO_P105.py ---
# Caterpillar's Command: Restoration of a second missing artifact.
# Timestamp: 2024-05-22 04:15:00 UTC
# Applicable Rules: All. The first working simulation of De-Rigidized Trigonometry.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import argparse

def run_resonant_circle_simulation(steps, pacer_speed_factor):
    """
    Simulates and visualizes the Resonant Circle, the Pacer Process,
    and the moments of Tangent Resonance.
    """
    print("--- RESONANT CIRCLE SIMULATOR v1.1 (Corrected) ---")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    plt.style.use('dark_background')
    
    # Setup for ax1
    ax1.set_xlim(-1.5, 1.5); ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal'); ax1.set_title("Resonant System", color='white')
    ax1.grid(color='gray', linestyle='--', alpha=0.3)
    circle_path = plt.Circle((0, 0), 1, color='cyan', fill=False, linestyle='--')
    ax1.add_artist(circle_path)
    
    system_point, = ax1.plot([], [], 'o', markersize=12, color='lime')
    potential_vector, = ax1.plot([], [], '-', lw=2, color='lime')
    pacer_line, = ax1.plot([], [], '-', lw=2, color='magenta', alpha=0.7)
    resonance_flash = ax1.scatter([], [], s=250, facecolors='none', edgecolors='yellow', lw=3)
    
    # Setup for ax2
    ax2.set_xlim(0, 2 * np.pi); ax2.set_ylim(0, 1)
    ax2.set_title("Chronospectrum Generation", color='white')
    ax2.set_xlabel("Process Angle (θ_p)", color='white'); ax2.set_yticks([])
    
    chronospectrum = []

    def update(frame):
        theta_p = (frame / steps) * 2 * np.pi
        x = np.cos(theta_p); y = np.sin(theta_p)
        pacer_angle = theta_p * pacer_speed_factor
        
        try:
            pacer_state = np.tan(pacer_angle)
            system_angle_state = np.tan(theta_p)
            is_close = np.isclose(pacer_state, system_angle_state, atol=0.05)
        except FloatingPointError: is_close = False

        system_point.set_data([x], [y])
        potential_vector.set_data([0, x], [0, y])
        
        pacer_x = np.cos(np.arctan(pacer_state)) if not np.isinf(pacer_state) else 0
        pacer_y = np.sin(np.arctan(pacer_state)) if not np.isinf(pacer_state) else 1 * np.sign(pacer_state)
        pacer_line.set_data([-pacer_x*1.5, pacer_x*1.5], [-pacer_y*1.5, pacer_y*1.5])
        
        if is_close:
            resonance_flash.set_offsets(np.array([[x, y]]))
            if not any(np.isclose(theta_p, val) for val in chronospectrum):
                chronospectrum.append(theta_p)
                ax2.axvline(theta_p, color='yellow', linestyle='-', alpha=0.5)
        else:
            resonance_flash.set_offsets(np.array([]).reshape(0, 2))
            
        return system_point, potential_vector, pacer_line, resonance_flash

    ani = FuncAnimation(fig, update, frames=steps, interval=20, blit=True, repeat=False)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resonant Circle Simulator v1.1")
    parser.add_argument("--steps", type=int, default=500)
    parser.add_argument("--pacer_speed", type=float, default=3.0)
    args = parser.parse_args()
    run_resonant_circle_simulation(args.steps, args.pacer_speed)