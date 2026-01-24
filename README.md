# Drone Swarm Simulation 🛸

A physics-based simulation of a massive drone swarm (1000 drones) performing formation control, complex transitions, and dynamic target tracking.

## 📖 Project Overview

This project simulates a swarm of quadcopters using **Ordinary Differential Equations (ODEs)** and **Potential Fields**.
The simulation enforces realistic physics constraints including maximum velocity, collision avoidance (repulsion), and smooth damping.

The project demonstrates three distinct capabilities:
1.  **Task 1: Formation Control** - Drones autonomously organize to form a static shape (a name) from an image input.
2.  **Task 2: Transition Flight** - The swarm smoothly transitions from the first formation into a new text formation ("Happy New Year!").
3.  **Task 3: Dynamic Tracking** - The swarm tracks a moving target (a figure-8 pattern) in real-time based on computer vision analysis of a video feed.

## Technologies Used
* **Python 3.10+**
* **NumPy:** High-performance vectorized physics calculations (forces, distances, velocities).
* **OpenCV (cv2):** Image processing and background subtraction for target extraction.
* **Matplotlib:** 3D and 2D visualization and animation.
* **Runge-Kutta 4 (RK4):** High-precision numerical integration solver for stability.
  
## Project Structure

```text
DroneShow_Project/
├── Data/
│   ├── input/                 # Input images (name.jpg) and videos (video.mp4)
│   └── output/                # Generated MP4 animations
│
├── src/
│   ├── __init__.py            # Package initialization
│   ├── config.py              # Physics constants (mass, Kp, Kd, dimensions)
│   ├── physics.py             # Vectorized force calculations (attraction / repulsion)
│   ├── solver.py              # Runge-Kutta 4 (RK4) integrator
│   ├── preprocessing.py       # Image-to-points logic
│   ├── video_processing.py    # Video-to-targets logic
│   └── visualizer.py          # Matplotlib animation logic
│
├── create_video.py             # Helper script to create test video for Task 3
├── main_task1.py               # Execution script for Task 1 (formation control)
├── main_task2.py               # Execution script for Task 2 (transition flight)
├── main_task3.py               # Execution script for Task 3 (dynamic tracking)
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
