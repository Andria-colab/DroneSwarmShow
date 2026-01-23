import numpy as np
import os  # <--- Added this to create folders
from src import (
    N_DRONES, DT, TOTAL_TIME, TASK_LIMITS, 
    get_target_points, compute_forces, rk4_step, 
    animate_swarm, animate_swarm_2d
)

def main():
    print(f"--- Starting Drone Show Simulation (Task 1) ---")
    
    # 1. SETUP: Get Target Points from Image
    image_path = "Data/input/name.jpg" 
    
    try:
        targets = get_target_points(image_path, n_drones=N_DRONES, z_height=10.0, scale=0.35)
        print(f"Targets generated successfully. Shape: {targets.shape}")
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return

    # 2. INITIALIZATION: Start on ground
    start_positions = np.random.rand(N_DRONES, 3) * 10.0
    start_positions[:, 0] -= 5.0
    start_positions[:, 1] -= 5.0
    start_positions[:, 2] = 0.0
    
    start_velocities = np.zeros((N_DRONES, 3))
    
    # 3. SIMULATION LOOP
    positions = start_positions.copy()
    velocities = start_velocities.copy()
    history = [positions.copy()]
    
    steps = int(TOTAL_TIME / DT)
    print(f"Simulating {steps} steps ({TOTAL_TIME} seconds)...")
    
    for step in range(steps):
        if step % (steps // 10) == 0:
            print(f"Progress: {step / steps * 100:.0f}%")
            
        positions, velocities = rk4_step(positions, velocities, targets, DT)
        history.append(positions.copy())
        
    print("Simulation complete. Saving videos...")
    
    # 4. VISUALIZATION & SAVING
    # Create output directory if it doesn't exist
    os.makedirs("Data/output", exist_ok=True)
    
    # Save 3D Video
    animate_swarm(history, TASK_LIMITS["task1"], filename="Data/output/task1_name_3d.mp4")
    
    # Save 2D Video
    animate_swarm_2d(history, TASK_LIMITS["task1"], filename="Data/output/task1_name_2d.mp4")
    
    
    print("All Done! Check the 'Data/output' folder.")

if __name__ == "__main__":
    main()