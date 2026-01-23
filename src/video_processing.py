import cv2
import numpy as np
import os

def extract_video_targets(video_path, n_drones, scale=0.1, z_height=10.0, sample_rate=5):
    """
    Reads a video and converts the moving object in each frame into drone targets.
    
    Args:
        sample_rate: Only process every X frames (to match simulation speed).
    Returns:
        np.array: Shape (num_frames, n_drones, 3)
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    cap = cv2.VideoCapture(video_path)
    
    # Background subtractor learns the background and masks moving objects
    back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=False)
    
    all_frame_targets = []
    frame_count = 0
    
    print("Processing video frames (this may take a moment)...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        if frame_count % sample_rate != 0:
            continue
            
        # 1. Get the Moving Object Mask
        fg_mask = back_sub.apply(frame)
        
        # Clean up noise
        kernel = np.ones((3,3), np.uint8)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        
        # 2. Extract Points from the Mask
        y_coords, x_coords = np.where(fg_mask > 200) # Threshold for white pixels
        points = np.column_stack((x_coords, y_coords))
        
        total_points = points.shape[0]
        
        # If no object is found in this frame, use the previous frame's targets
        # (Or zeros if it's the first frame)
        if total_points < 10:
            if len(all_frame_targets) > 0:
                all_frame_targets.append(all_frame_targets[-1])
            continue

        # 3. Downsample to N drones
        # Use replacement if the object is small (fewer pixels than drones)
        indices = np.random.choice(total_points, n_drones, replace=(total_points < n_drones))
        selected = points[indices]
        
        # 4. Center and Scale
        # We center based on the FRAME size, not the object center, 
        # so movement across the screen is preserved.
        h, w = frame.shape[:2]
        x_centered = selected[:, 0] - (w / 2)
        y_centered = selected[:, 1] - (h / 2)
        
        frame_targets = np.zeros((n_drones, 3))
        frame_targets[:, 0] = x_centered * scale
        frame_targets[:, 1] = -y_centered * scale
        frame_targets[:, 2] = z_height
        
        all_frame_targets.append(frame_targets)
        
    cap.release()
    print(f"Extracted {len(all_frame_targets)} frames of target data.")
    return np.array(all_frame_targets)