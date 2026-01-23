import numpy as np

# --- Simulation Parameters ---
# Number of drones (You must determine this based on your name image)
# Start with a safe number, we will update this dynamically in preprocessing later.
N_DRONES = 500

# Time step for the simulation (keep it small for stability)
DT = 0.01  

# Total simulation time (in seconds)
TOTAL_TIME = 20.0  

# --- Physics Constants (from PDF Page 8) ---
# [cite_start]Mass of each drone (assumed uniform) [cite: 103]
MASS = 1.0  

# [cite_start]Maximum velocity magnitude [cite: 105]
V_MAX = 5.0  

# [cite_start]Attraction Gain (kp): How strongly they fly toward targets [cite: 62]
K_P = 2.0  

# [cite_start]Damping Coefficient (kd): Prevents infinite oscillation [cite: 68]
K_D = 1.5  

# [cite_start]Repulsion Gain (k_rep): Strength of collision avoidance [cite: 108]
K_REP = 10.0  

# [cite_start]Safety Radius (R_safe): Distance where repulsion activates [cite: 109]
R_SAFE = 0.8  

# --- Canvas/Space Parameters ---
# This defines the 3D box where drones can fly
# Example: x from -10 to 10, y from -10 to 10, z from 0 to 20
SPACE_LIMITS = ((-80, 80), (-80, 80), (0, 20))