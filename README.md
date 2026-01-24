# Drone Swarm Simulation 🛸

A physics-based simulation of a massive drone swarm (1000 drones) performing formation control, complex transitions, and dynamic target tracking.

## 📖 Project Overview

This project simulates a swarm of quadcopters using **Ordinary Differential Equations (ODEs)** and **Potential Fields**. The simulation enforces realistic physics constraints including maximum velocity, collision avoidance (repulsion), and smooth damping.

The project demonstrates three distinct capabilities:
1.  **Task 1: Formation Control** - Drones autonomously organize to form a static shape (a name) from an image input.
2.  **Task 2: Transition Flight** - The swarm smoothly transitions from the first formation into a new text formation ("Happy New Year!").
3.  **Task 3: Dynamic Tracking** - The swarm tracks a moving target (a figure-8 pattern) in real-time based on computer vision analysis of a video feed.

## 🛠️ Technologies Used
* **Python 3.10+**
* **NumPy:** High-performance vectorized physics calculations (forces, distances, velocities).
* **OpenCV (cv2):** Image processing and background subtraction for target extraction.
* **Matplotlib:** 3D and 2D visualization and animation.
* **Runge-Kutta 4 (RK4):** High-precision numerical integration solver for stability.

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/Andria-colab/DroneShow_Project.git](https://github.com/Andria-colab/DroneShow_Project.git)
cd DroneShow_Project

2. Set up a Virtual Environment (Recommended)Bashpython -m venv venv
# Activate on Mac/Linux:
source venv/bin/activate
# Activate on Windows:
# venv\Scripts\activate

3. Install DependenciesBashpip install -r requirements.txt

4. Install FFmpegRequired for saving the simulation animations as MP4 videos.Mac (Homebrew): brew install ffmpegWindows: Download from ffmpeg.org or use choco install ffmpeg.Linux: sudo apt install ffmpeg🏃 How to Run the SimulationsTask 1: Name FormationGenerates the drone targets from Data/input/name.jpg and simulates the formation.Bashpython main_task1.py

Output: 2D and 3D videos of drones forming the name "Andria Beridze" in Data/output/.Task 2: Transition to GreetingSimulates the transition flight. Drones start at the "Name" formation and fly to form the text "Happy New Year!".Bashpython main_task2.py

Output: Videos showing the smooth transition between shapes.Task 3: Dynamic Video TrackingFirst, generate the input video (a moving white circle), then run the tracking simulation.Bash# Step 1: Generate the test video (40 seconds)
python create_video.py

# Step 2: Run the simulation
python main_task3.py
Output: Videos of the swarm chasing the moving object in a figure-8 pattern.📂 Project StructurePlaintextDroneShow_Project/
├── Data/
│   ├── input/           # Input images (name.jpg) and videos (video.mp4)
│   └── output/          # Generated MP4 animations are saved here
├── src/
│   ├── __init__.py      # Package initialization
│   ├── config.py        # Physics constants (Mass, Kp, Kd) and Dimensions
│   ├── physics.py       # Vectorized force calculations (Attraction/Repulsion)
│   ├── solver.py        # Runge-Kutta 4 (RK4) integrator
│   ├── preprocessing.py # Image-to-points logic
│   ├── video_processing.py # Video-to-targets logic
│   └── visualizer.py    # Matplotlib animation logic
├── create_video.py      # Helper script to create test video for Task 3
├── main_task1.py        # Execution script for Task 1
├── main_task2.py        # Execution script for Task 2
├── main_task3.py        # Execution script for Task 3
├── requirements.txt     # List of python libraries
└── README.md            # Project documentation

Physics ModelThe motion of each drone $i$ is governed by the following Second-Order ODE:$$m \ddot{r}_i = F_{att} + F_{damp} + F_{rep}$$Attraction ($F_{att}$): Proportional control pulling the drone toward its target position ($K_p \cdot (r_{target} - r_i)$).Damping ($F_{damp}$): Viscous friction to prevent infinite oscillations ($K_d \cdot v_i$).Repulsion ($F_{rep}$): Inverse-cube law forces that activate when drones get too close ($< R_{safe}$), preventing collisions.ConfigurationYou can adjust the physics and simulation parameters in src/config.py:N_DRONES: Number of drones (set to 1000).TOTAL_TIME: Duration of the simulation.TASK_LIMITS: Viewing boundaries for the 2D/3D plots.