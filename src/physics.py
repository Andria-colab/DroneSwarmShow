import numpy as np
from .config import MASS, K_P, K_D, K_REP, R_SAFE, V_MAX

def velocity_saturation(v):
    """
    Limits the velocity to V_MAX.
    """
    norm_v = np.linalg.norm(v)
    if norm_v > V_MAX:
        return v * (V_MAX / norm_v)
    return v

def compute_forces(positions, velocities, targets):
    """
    Calculates forces using fast Vectorized Matrix Math (No loops!).
    """
    # 1. Attraction & Damping
    attraction = K_P * (targets - positions)
    damping = -K_D * velocities
    
    # 2. Vectorized Repulsion 
    # Instead of a loop, we compute all distances at once using broadcasting.
    
    # Create matrix of all position differences (N x N x 3)
    # shape: (N, 1, 3) - (1, N, 3) -> (N, N, 3)
    diff_matrix = positions[:, np.newaxis, :] - positions[np.newaxis, :, :]
    
    # Compute Distance Matrix (N x N)
    dist_matrix = np.linalg.norm(diff_matrix, axis=2)
    
    # Fill diagonal with Infinity so drones don't repel themselves
    np.fill_diagonal(dist_matrix, np.inf)
    
    # Find pairs that are too close
    mask = dist_matrix < R_SAFE
    
    repulsion = np.zeros_like(positions)
    
    if np.any(mask):
        # Calculate 1 / distance^3 safely
        # We only care about distances where mask is True
        with np.errstate(divide='ignore'):
            inv_dist_cubed = 1.0 / (dist_matrix ** 3)
        
        # Zero out entries that aren't close enough
        inv_dist_cubed[~mask] = 0.0
        
        # Calculate Force Vectors: direction * strength
        # (N, N, 3) * (N, N, 1) -> (N, N, 3)
        force_matrix = diff_matrix * inv_dist_cubed[:, :, np.newaxis]
        
        # Sum all repulsive forces acting on each drone (Sum over axis 1)
        repulsion = K_REP * np.sum(force_matrix, axis=1)

    # 3. Total Force
    total_force = attraction + damping + repulsion
    accelerations = total_force / MASS
    
    return accelerations