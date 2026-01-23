import numpy as np

# --- Simulation Parameters ---
# Number of drones (Updated to 1000 as per your settings)
N_DRONES = 1000

# Time step for the simulation
DT = 0.01  

# Total simulation time (Increased to 40.0s to give them time to move)
TOTAL_TIME = 60.0  

# --- Physics Constants ---
# Mass of each drone
MASS = 1.0  

# Maximum velocity magnitude
V_MAX = 5.0  

# Attraction Gain (kp): Strength of flight toward targets
K_P = 2.0  

# Damping Coefficient (kd): Stabilizes movement
K_D = 1.5  

# Repulsion Gain (k_rep): Strength of collision avoidance
K_REP = 10.0  

# Safety Radius (R_safe): Distance where repulsion activates
R_SAFE = 0.8  

# --- GRAPH DIMENSIONS (Updated) ---
# Replaces SPACE_LIMITS. 
# Allows each task to have its own boundary size.
# Format: ((min_x, max_x), (min_y, max_y), (min_z, max_z))

TASK_LIMITS = {
    # Task 1 (Name): Wide X to fit "Andria Beridze"
    "task1": ((-300, 300), (-100, 100), (0, 20)),   
    
    # Task 2 (Greeting): Very wide X to fit "Happy New Year!"
    "task2": ((-100, 100), (-40, 40), (0, 20)),   
    
    # Task 3 (Video): Usually square, so we keep X and Y equal
    "task3": ((-100, 100), (-100, 100), (0, 30)),   
}