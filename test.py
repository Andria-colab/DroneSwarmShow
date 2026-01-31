import numpy as np
import os
from src import (
    N_DRONES, DT, TASK_LIMITS,
    get_text_points, extract_video_targets,
    rk4_step, animate_swarm, animate_swarm_2d, count_collisions
)

def main():
    print(f"--- Starting Task 3: Dynamic Video Tracking ---")
    
    # 1. SETUP
    video_path = "Data/input/video.mp4"
    
    # 2. LOAD VIDEO TARGETS
    print("Extracting video frames...")
    try:
        # Sample every 2nd frame to reduce total frames
        video_frames = extract_video_targets(video_path, n_drones=N_DRONES, scale=0.8, sample_rate=2)
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
    start_targets = get_text_points("Happy New Year!", n_drones=N_DRONES, scale=0.8)
    
    positions = start_targets.copy()
    velocities = np.zeros((N_DRONES, 3))
    
    history = [positions.copy()]
    
    # 4. TRANSITION PHASE - Move from text to first ball position
    print("Transitioning from text to ball...")
    first_ball_position = video_frames[0]
    transition_steps = 300  # Reduced: 3 seconds transition
    
    for step in range(transition_steps):
        positions, velocities = rk4_step(positions, velocities, first_ball_position, DT)
        history.append(positions.copy())
        
        if step % 100 == 0:
            print(f"Transition progress: {step / transition_steps * 100:.0f}%")
    
    print("Transition complete! Starting ball tracking...")
    
    # 5. BALL TRACKING SIMULATION
    # Calculate steps_per_frame to hit 120 seconds total
    # 120 seconds total - 3 seconds transition = 117 seconds for tracking
    # 117 seconds / DT / num_video_frames = steps per frame
    target_tracking_time = 117  # seconds
    steps_per_frame = int(target_tracking_time / (DT * num_video_frames))
    
    total_steps = num_video_frames * steps_per_frame
    print(f"Simulating {total_steps} steps (approx {total_steps * DT:.1f} seconds)...")

    crashes_total = 0
    
    for frame_idx in range(num_video_frames):
        current_target = video_frames[frame_idx]
        
        for step in range(steps_per_frame):
            positions, velocities = rk4_step(positions, velocities, current_target, DT)
            history.append(positions.copy())

            crashes = count_collisions(positions, limit=0.2)
            if crashes > 0:
                crashes_total += crashes
            
        if frame_idx % 20 == 0:
            print(f"Tracking progress: {frame_idx / num_video_frames * 100:.0f}%")

    # 6. SAVE
    total_time = len(history) * DT
    print(f"\nSimulation complete!")
    print(f"Total frames: {len(history)}")
    print(f"Total time: {total_time:.1f} seconds")
    
    if crashes_total == 0:
        print("✓ No crashes detected during the simulation.")
    else:
        print(f"⚠ Total crashes: {crashes_total}")
    
    print("\nSaving videos...")
    os.makedirs("Data/output", exist_ok=True)
    
    animate_swarm(history, TASK_LIMITS["task3"], filename="Data/output/task3_video_3d.mp4")
    animate_swarm_2d(history, TASK_LIMITS["task3"], filename="Data/output/task3_video_2d.mp4")
    print("Done! Check Data/output folder.")

if __name__ == "__main__":
    main()