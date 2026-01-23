# src/__init__.py

# This allows you to do:
# from src import get_target_points, compute_forces, runge_kutta_step
# Instead of:
# from src.preprocessing import get_target_points

from .config import *
from .preprocessing import get_target_points
from .physics import compute_forces, velocity_saturation
from .solver import rk4_step
from .visualizer import animate_swarm, animate_swarm_2d