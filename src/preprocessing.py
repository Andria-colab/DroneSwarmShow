import numpy as np
import cv2
import os

def get_target_points(image_path, n_drones, z_height=10.0, scale=0.1):
    """
    Extracts N target points (x, y, z) from a handwritten name image.
    """
    
    # 1. Load the image in grayscale
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at: {image_path}")
        
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # 2. IMPROVED: Adaptive Thresholding
    # This looks at local neighborhoods to separate ink from paper shadows.
    # 11 is the block size, 10 is the constant subtracted from the mean.
    binary = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 15, 10)

    # Clean up small noise dots (Morphological Opening)
    kernel = np.ones((3,3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # 3. Find coordinates of all non-zero pixels (the text)
    y_coords, x_coords = np.where(binary > 0)
    all_points = np.column_stack((x_coords, y_coords))
    
    total_points = all_points.shape[0]
    
    if total_points < n_drones:
        print(f"Warning: Found only {total_points} pixels. Using all of them.")
        n_drones = total_points # Adjust if we don't have enough pixels
        
    # 4. Downsample: Select exactly N points
    indices = np.random.choice(total_points, n_drones, replace=False)
    selected_points = all_points[indices]
    
    # 5. Convert to 3D Coordinates (x, y, z)
    # Center the name at (0,0)
    x_centered = selected_points[:, 0] - np.mean(selected_points[:, 0])
    y_centered = selected_points[:, 1] - np.mean(selected_points[:, 1])
    
    targets = np.zeros((n_drones, 3))
    targets[:, 0] = x_centered * scale
    targets[:, 1] = -y_centered * scale  # Flip Y 
    targets[:, 2] = z_height
    
    return targets

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    # Matches your folder structure
    TEST_IMAGE = "Data/input/name.jpg" 
    
    # Temporarily set N higher for testing
    targets = get_target_points(TEST_IMAGE, n_drones=600) 
    print(f"Generated {len(targets)} targets.")
    
    plt.figure(figsize=(10, 4)) # Wide aspect ratio for text
    plt.scatter(targets[:, 0], targets[:, 1], s=5, c='black')
    plt.title("Drone Target Positions")
    plt.xlabel("X (meters)")
    plt.ylabel("Y (meters)")
    plt.axis('equal') # Crucial: Keeps the text from looking squashed
    plt.grid(True)
    plt.show()