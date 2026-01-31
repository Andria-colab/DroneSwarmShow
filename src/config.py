import numpy as np

# --- Simulation Parameters ---
# Number of drones (Updated to 1000 as per your settings)
N_DRONES = 1000

# Time step for the simulation
DT = 0.01  

# Total simulation time (Increased to 40.0s to give them time to move)
TOTAL_TIME = 100.0  

# --- Physics Constants (SAFE MODE) ---
MASS = 1.0  

# 1. SLOW DOWN: Reduce Max Speed (was 5.0)
V_MAX = 5.0  

# 2. GENTLE PULL: Reduce Attraction so they don't rush (was 2.0)
K_P = 1.0  

# 3. HEAVY BRAKING: Increase Damping to stop oscillations (was 1.5)
K_D = 4.0  

# 4. STRONG SHIELD: Massive Repulsion to prevent overlapping (was 10.0)
# This is the most important change!
K_REP = 200.0  

# 5. EARLY WARNING: Start repelling sooner (was 0.8)
R_SAFE = 1.2

# --- GRAPH DIMENSIONS (Updated) ---
# Replaces SPACE_LIMITS. 
# Allows each task to have its own boundary size.
# Format: ((min_x, max_x), (min_y, max_y), (min_z, max_z))

TASK_LIMITS = {
    # Task 1 (Name): Wide X to fit "Andria Beridze"
    "task1": ((-300, 300), (-100, 100), (0, 20)),   
    
    # Task 2 (Greeting): Very wide X to fit "Happy New Year!"
    "task2": ((-120, 120), (-120, 120), (0, 20)),   
    
    # Task 3 (Video): Usually square, so we keep X and Y equal
    "task3": ((-120, 120), (-120, 120), (0, 30)),   
}