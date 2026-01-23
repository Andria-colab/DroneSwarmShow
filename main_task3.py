import numpy as np
import os
from src import (
    N_DRONES, DT, TASK_LIMITS,
    get_text_points, extract_video_targets,
    rk4_step, animate_swarm, animate_swarm_2d
)

def main():
    print(f"--- Starting Task 3: Dynamic Video Tracking ---")
    
    # 1. SETUP
    video_path = "Data/input/video.mp4"
    
    # 2. LOAD VIDEO TARGETS
    print("Extracting video frames (reading EVERY frame for smooth timing)...")
    try:
        # CHANGE 1: Set sample_rate=1 to use every single frame of the 40s video
        video_frames = extract_video_targets(video_path, n_drones=N_DRONES, scale=0.2, sample_rate=1)
    except Exception as e:
        print(f"Error: {e}")
        return

    num_video_frames = len(video_frames)
    if num_video_frames == 0:
        print("No moving object detected in video!")
        return

    print(f"Loaded {num_video_frames} frames from video.")

    # 3. INITIALIZATION (Start at "Happy New Year")
    print("Initializing at 'Happy New Year'...")
    start_targets = get_text_points("Happy New Year!", n_drones=N_DRONES, scale=0.3)
    
    positions = start_targets.copy()
    velocities = np.zeros((N_DRONES, 3))
    
    history = [positions.copy()]
    
    # 4. SIMULATION LOOP
    # CHANGE 2: Sync Physics to Video FPS
    # Video is 30 FPS -> 1 frame = 0.033 seconds
    # Simulation DT is 0.01 seconds
    # We need approx 3 or 4 simulation steps to equal 1 video frame.
    steps_per_frame = 3 
    
    total_steps = num_video_frames * steps_per_frame
    print(f"Simulating {total_steps} steps (approx {total_steps * DT:.1f} seconds)...")

    for frame_idx in range(num_video_frames):
        # Update the target to the current video frame
        current_target = video_frames[frame_idx]
        
        # Run physics for a tiny bit of time to catch up to the frame
        for _ in range(steps_per_frame):
            positions, velocities = rk4_step(positions, velocities, current_target, DT)
            history.append(positions.copy())
            
        if frame_idx % 100 == 0:
            print(f"Progress: {frame_idx / num_video_frames * 100:.0f}%")

    # 5. SAVE
    print("Saving videos...")
    os.makedirs("Data/output", exist_ok=True)
    
    # Use Task 3 specific limits
    animate_swarm(history, TASK_LIMITS["task3"], filename="Data/output/task3_video_3d.mp4")
    animate_swarm_2d(history, TASK_LIMITS["task3"], filename="Data/output/task3_video_2d.mp4")
    print("Done! Check Data/output folder.")

if __name__ == "__main__":
    main()