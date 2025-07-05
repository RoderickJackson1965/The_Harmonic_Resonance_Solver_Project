# --- CSO_P114.py (Corrected) ---
# Caterpillar's Command: The Final, Corrected "Flow-Stop" Resonance Simulator
# Timestamp: 2024-05-22 01:25:00 UTC
# Applicable Rules: All. A final, corrected model with proper boundary handling.

import numpy as np
import matplotlib.pyplot as plt
import argparse

def run_flow_stop_simulation(num_steps, initial_velocity):
    """
    Simulates an emergent orbit and finds the 4 Flow-Stop resonances.
    """
    print(f"--- FLOW-STOP RESONANCE SIMULATOR (v2.1) ---")
    
    # 1. Initial Conditions & Simulation
    position = np.array([1.0, 0.0])
    velocity = np.array([0.0, initial_velocity])
    path_history = []
    velocity_history = []
    
    for _ in range(num_steps):
        path_history.append(position)
        velocity_history.append(velocity)
        force = -position
        velocity = velocity + (0.01 * force) # Using a fixed small time_step
        position = position + (0.01 * velocity)
        
    path_history = np.array(path_history)
    velocity_history = np.array(velocity_history)
    vx = velocity_history[:, 0]
    vy = velocity_history[:, 1]

    # 2. Find moments of Flow-Stop Resonance
    vx_zero_crossings = np.where(np.diff(np.sign(vx)))[0]
    vy_zero_crossings = np.where(np.diff(np.sign(vy)))[0]
    resonance_indices = np.sort(np.unique(np.concatenate([vx_zero_crossings, vy_zero_crossings])))
    
    # 3. Visualization
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.style.use('dark_background'); ax.set_aspect('equal')
    ax.set_title("Flow-Stop Resonances of an Emergent Orbit", color='white')
    ax.grid(color='gray', linestyle='--', alpha=0.3)
    ax.plot(path_history[:, 0], path_history[:, 1], '-', color='cyan', lw=1.5)
    if resonance_indices.size > 0:
        ax.scatter(path_history[resonance_indices, 0], path_history[resonance_indices, 1],
                   s=200, c='yellow', marker='*', zorder=10, label='Flow-Stop Resonance')
    ax.legend()
    plt.show()
    
    # 4. Reporting
    print("\n--- SIMULATION COMPLETE ---")
    print(f"Generated a Chronospectrum with {len(resonance_indices)} resonance points.")
    print("------------------------------------------")
    for i, step_index in enumerate(resonance_indices):
        angle = np.rad2deg(np.arctan2(path_history[step_index,1], path_history[step_index,0]))
        # Normalize angle to be positive
        angle = (angle + 360) % 360
        print(f"  Resonance {i+1} at step {step_index}, Angle ≈ {angle:.2f}°")
    print("------------------------------------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flow-Stop Resonance Simulator.")
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--velocity", type=float, default=1.0, help="Initial upward velocity.")
    args = parser.parse_args()
    # --- TYPO FIX IS HERE ---
    run_flow_stop_simulation(args.steps, args.velocity)
    # --- END OF FIX ---