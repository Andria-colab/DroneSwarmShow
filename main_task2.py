# main_task2.py
import numpy as np
import os
from src import (
    N_DRONES, DT, TOTAL_TIME, TASK_LIMITS, 
    get_target_points, get_text_points,
    rk4_step, animate_swarm, animate_swarm_2d, count_collisions 
)

def main():
    print(f"--- Starting Task 2: Transition to Greeting ---")
    
    # 1. SETUP & LOAD INPUTS
    print("Loading Start Formation (Name)...")
    image_path = "Data/input/name.jpg"
    try:
        # Reduced scale to 0.4 to fit in the 300m box
        name_targets = get_target_points(image_path, n_drones=N_DRONES, z_height=10.0, scale=0.4)
    except Exception as e:
        print(f"Error loading name image: {e}")
        return

    print("Generating Target Formation (Greeting)...")
    # Reduced scale to 0.4 to fit in the 300m box
    greeting_targets = get_text_points("Happy New Year!", n_drones=N_DRONES, z_height=10.0, scale=0.4)

    # 2. INITIALIZATION
    positions = name_targets.copy()
    velocities = np.zeros((N_DRONES, 3))
    history = [positions.copy()]
    
    steps = int(TOTAL_TIME / DT)
    print(f"Simulating transition ({TOTAL_TIME} seconds)...")
    
    for step in range(steps):
        if step % (steps // 10) == 0:
            print(f"Progress: {step / steps * 100:.0f}%")
            
        positions, velocities = rk4_step(positions, velocities, greeting_targets, DT)
        history.append(positions.copy())

        # COLLISION CHECK (Limit 0.15m)
        crashes = count_collisions(positions, limit=0.15)
        if crashes > 0:
            print(f"CRASH: {crashes} pairs collided at step {step}!")
            
    if crashes == 0:
        print("No crashes detected during the simulation.")
    print("Simulation complete. Saving videos...")
    
    # 4. SAVE RESULTS
    os.makedirs("Data/output", exist_ok=True)
    
    # These functions now use the new 300x300 limits from config.py
    animate_swarm(history, TASK_LIMITS["task2"], filename="Data/output/task2_greeting_3d.mp4")
    animate_swarm_2d(history, TASK_LIMITS["task2"], filename="Data/output/task2_greeting_2d.mp4")
    print("All Done!")

if __name__ == "__main__":
    main()