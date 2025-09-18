# Virus Transmission Simulation

A Python simulation of pedestrians on a sidewalk, modeling avoidance behavior to mimic virus transmission dynamics, visualized with Matplotlib.

## Author
- **Aryan Chawla** - Data Science & Analytics Student  
  📧 Email: [axy.prof@gmail.com]  
  🔗 LinkedIn: [https://www.linkedin.com/in/aryan-chawla19/]  
  🐙 GitHub: [https://github.com/AryanChawla01]

## Project Overview

This project simulates pedestrians moving eastward and westward on a 2D sidewalk grid. Agents avoid opposing team members within a set distance to simulate social distancing, displayed as a real-time animation.

## Technologies Used

- Python 3.9
- Matplotlib (for animation)
- Random (for agent behavior)
- Object-oriented programming

## File Structure

Virus-Transmission-Simulation/  
├── virus_transmission_simulation.py # Simulation code  
├── README.md # Project documentation  
├── output figure.png #sample output screenshot

## Skills Demonstrated

- Agent-based simulation design
- Object-oriented programming
- Matplotlib animation
- Grid-based spatial modeling
- Random processes for agent movement

## Simulation Features

- **Agent Movement**: Eastward agents move right, westward agents move left. Agents avoid opposing teams within a concern distance (default: 4 units) unless enough teammates are nearby (default: 5).
- **Dynamic Entry**: New agents enter randomly based on an interarrival rate (default: every 3 steps).
- **Visualization**: Real-time animation shows eastward agents in green and westward in red on a grey sidewalk grid.
- **Configurable Parameters**: Adjust sidewalk size, concern distance, safe threshold, and interarrival rate in the code.

## Requirements

- Python 3.9 or higher
- Matplotlib (`pip install matplotlib`)

## Getting Started

1. Install dependencies:
   ```bash
   pip install matplotlib
   ```

2. Run the simulation:
   ```bash
   python virus_transmission_simulation.py
   ```

3. Customize (optional):
   - Modify `SIDEWALK_WIDTH`, `SIDEWALK_LENGTH`, `INTERARRIVAL`, `CONCERN_DISTANCE`, or `SAFE_THRESHOLD` in `virus_transmission_simulation.py`.

## How It Works

- **Sidewalk Grid**: A 200x25 grid where agents move and interact.
- **Behavior**: Agents move toward their destination but shift to avoid opposing agents within the concern distance.
- **Animation**: Matplotlib displays the simulation with a 50ms interval over 2000 frames.
