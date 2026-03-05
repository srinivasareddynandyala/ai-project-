# AI Project - Comprehensive Assignment

This project implements comprehensive AI solutions for three main tasks:

## Task 1: Turing Test and CAPTCHA Architecture Design

### Objective
Design and document an appropriate architecture for implementing Turing Test and CAPTCHA systems.

### Key Components
- **Turing Test Implementation**: Architecture for human vs machine differentiation
- **CAPTCHA Design**: Security mechanisms to prevent automated access

### Architecture Overview
See `task1_turing_captcha_architecture.md` for detailed architecture design.

---

## Task 2: Reflex Agent with Environmental Parameters

### Objective
Design and develop a simple reflex agent that takes environmental parameters from sensors and reports AQI (Air Quality Index) in a region.

### Key Features
- **Sensor Integration**: Reads environmental data from files/sensors
- **AQI Calculation**: Calculates Air Quality Index based on pollutant levels
- **Reflex Logic**: Simple stimulus-response behavior
- **Reporting**: Reports AQI levels and recommendations

### Implementation
See `task2_reflex_agent_aqi.py` for the reflex agent implementation.

---

## Task 3: Uninformed Search Algorithms

### Objective
Implement BFS, DFS and their variants to solve classic AI search problems and compare their performance.

### Search Problems
1. **Tic Tac Toe**: Game state search
2. **Eight Queens**: Constraint satisfaction
3. **Milk and Water Jug**: State space search
4. **Missionaries and Cannibals**: River crossing puzzle

### Algorithms Implemented
- **BFS (Breadth-First Search)**: Level-by-level exploration
- **DFS (Depth-First Search)**: Deep exploration
- **DFS Iterative**: Depth-limited variant
- **IDDFS**: Iterative deepening with optimality

### Implementation Files
- `task3_search_algorithms.py`: Core algorithm implementations
- `task3_search_problems.py`: Problem definitions
- `task3_test_comparison.py`: Test suite and performance comparison

---

## Project Structure

```
ai-project/
├── README.md (this file)
├── task1_turing_captcha_architecture.md
├── task2_reflex_agent_aqi.py
├── task3_search_algorithms.py
├── task3_search_problems.py
└── task3_test_comparison.py
```

## Technologies Used
- Python 3.x
- Standard libraries (collections, time, typing)

## How to Run

### Task 2: Reflex Agent
```bash
python task2_reflex_agent_aqi.py
```

### Task 3: Search Algorithms
```bash
python task3_test_comparison.py
```

## Performance Metrics

All implementations include:
- Execution time tracking
- Memory usage monitoring
- Performance comparison tables
- Detailed metrics reporting

---

## References
- Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach
- Air Quality Index Standards (EPA, AQI guidelines)
- Classical AI Problem Solvers
