import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .config import DT


def animate_swarm(history_positions, limits, filename=None):
    """ Standard 3D Animation with custom limits """
    print(f"Preparing 3D animation...")
    skip_frames = 5
    frames = history_positions[::skip_frames]
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Unpack the specific limits for this task
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = limits
    
    scatter = ax.scatter([], [], [], c='blue', s=5)
    
    def init():
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_zlim(z_min, z_max)
        ax.set_xlabel('X (meters)')
        ax.set_ylabel('Y (meters)')
        ax.set_zlabel('Z (meters)')
        ax.set_title("Drone Swarm (3D View)")
        return scatter,

    def update(frame_idx):
        current_pos = frames[frame_idx]
        scatter._offsets3d = (current_pos[:, 0], current_pos[:, 1], current_pos[:, 2])
        ax.set_title(f"3D View - Time: {frame_idx * DT * skip_frames:.2f} s")
        return scatter,

    ani = FuncAnimation(fig, update, frames=len(frames), init_func=init, blit=False, interval=30)
    
    if filename:
        print(f"Saving 3D video to {filename}...")
        ani.save(filename, writer='ffmpeg', fps=30)
        print("3D Video saved!")

def animate_swarm_2d(history_positions, limits, filename=None):
    """ Top-Down 2D Animation with custom limits """
    print(f"Preparing 2D animation...")
    skip_frames = 5
    frames = history_positions[::skip_frames]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Unpack limits (ignore Z for 2D view)
    (x_min, x_max), (y_min, y_max), _ = limits
    
    scatter = ax.scatter([], [], c='red', s=10)
    
    def init():
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_xlabel('X (meters)')
        ax.set_ylabel('Y (meters)')
        ax.set_title("Drone Swarm (Top-Down 2D View)")
        ax.grid(True)
        return scatter,

    def update(frame_idx):
        current_pos = frames[frame_idx]
        scatter.set_offsets(current_pos[:, :2])
        ax.set_title(f"2D View - Time: {frame_idx * DT * skip_frames:.2f} s")
        return scatter,

    ani = FuncAnimation(fig, update, frames=len(frames), init_func=init, blit=True, interval=30)
    
    if filename:
        print(f"Saving 2D video to {filename}...")
        ani.save(filename, writer='ffmpeg', fps=30)
        print("2D Video saved!")