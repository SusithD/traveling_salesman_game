# Traveling Salesman Game

An interactive educational game that demonstrates different algorithms for solving the Traveling Salesman Problem (TSP).

## Overview

This application allows users to:
- Select cities on a map
- Calculate optimal routes using three different algorithms:
  - Brute Force (exact solution)
  - Nearest Neighbor (greedy heuristic)
  - Dynamic Programming (exact solution using Held-Karp algorithm)
- Visualize and compare the results
- Save high scores in a database

## Project Structure

```
traveling_salesman_game/
├── algorithms/        # Algorithm implementations
├── core/              # Core functionality
├── database/          # Database management
├── gui/               # User interface components
├── utils/             # Utility functions
├── main.py            # Entry point
└── requirements.txt   # Dependencies
```

## Installation

1. Clone this repository
```bash
git clone https://github.com/yourusername/traveling_salesman_game.git
cd traveling_salesman_game
```

2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

## Features

- Interactive city selection on a map
- Multiple algorithm implementations with complexity analysis
- Real-time route visualization
- Performance comparison between algorithms
- High score tracking

## License

[MIT](LICENSE)