import numpy as np
from .physics import compute_forces, velocity_saturation

def rk4_step(positions, velocities, targets, dt):
    """
    Performs one time step of integration using Runge-Kutta 4 (RK4).
    """
    # Helper to apply saturation to a whole array of velocities
    def saturate_all(vel_array):
        return np.array([velocity_saturation(v) for v in vel_array])

    # 1. Calculate k1 (Slope at the beginning)
    k1_v = compute_forces(positions, velocities, targets)
    k1_x = velocities

    # 2. Calculate k2 (Slope at the midpoint, using k1)
    v_k1 = velocities + k1_v * 0.5 * dt
    x_k1 = positions + k1_x * 0.5 * dt
    v_k1 = saturate_all(v_k1) # Enforce speed limit
    
    k2_v = compute_forces(x_k1, v_k1, targets)
    k2_x = v_k1

    # 3. Calculate k3 (Another slope at the midpoint, using k2)
    v_k2 = velocities + k2_v * 0.5 * dt
    x_k2 = positions + k2_x * 0.5 * dt
    v_k2 = saturate_all(v_k2)
    
    k3_v = compute_forces(x_k2, v_k2, targets)
    k3_x = v_k2

    # 4. Calculate k4 (Slope at the end, using k3)
    v_k3 = velocities + k3_v * dt
    x_k3 = positions + k3_x * dt
    v_k3 = saturate_all(v_k3)
    
    k4_v = compute_forces(x_k3, v_k3, targets)
    k4_x = v_k3

    # 5. Weighted Average of slopes to get final state
    # new = old + (dt/6) * (k1 + 2k2 + 2k3 + k4)
    new_velocities = velocities + (dt / 6.0) * (k1_v + 2*k2_v + 2*k3_v + k4_v)
    new_positions = positions + (dt / 6.0) * (k1_x + 2*k2_x + 2*k3_x + k4_x)

    # Final speed check
    new_velocities = saturate_all(new_velocities)

    return new_positions, new_velocities