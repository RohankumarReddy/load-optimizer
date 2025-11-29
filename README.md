<h1 align="center">Disaster Relief Optimization – Fractional Knapsack</h1>

<p align="center">
  <img src="truck.gif" width="260" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/Data-Pandas-150458?style=for-the-badge&logo=pandas" />
  <img src="https://img.shields.io/badge/Charts-Plotly-3F4F75?style=for-the-badge&logo=plotly" />
</p>

---

## Overview

This project implements a **Fractional Knapsack–based optimization tool** to assist in planning and managing disaster-relief logistics.  
It helps determine how to **maximize the utility of relief items** when truck capacity is limited.  
The system is built using **Streamlit**, enabling real-time interaction, visualization, and CSV integration.

The tool is designed for organizations and agencies that require **efficient decision-making** during emergency resource distribution.

---

## Features

- Supports **manual data entry** and **CSV upload**
- Uses the **Fractional Knapsack Algorithm** to compute the optimal loading strategy
- Generates a detailed **load plan table** with quantities taken
- Displays **total utility score**
- Provides an interactive **Plotly bar chart** for load visualization
- Clean and intuitive **Streamlit UI**
- Works for any number of items and capacities

---

## Tech Stack

| Component | Technology | Purpose |
|----------|------------|---------|
| **Frontend Framework** | Streamlit | UI, forms, layout, user interaction |
| **Backend Logic** | Python | Core calculations and data processing |
| **Data Handling** | Pandas | Reading, structuring, cleaning item data |
| **Visualization** | Plotly Express | Interactive charts for utility and weights |


---

## How It Works

1. The user submits relief item data:  
   - Item name  
   - Weight  
   - Importance / Utility  

2. The system calculates the **importance-to-weight ratio** for every item.

3. Items are **sorted in descending order of utility density**.

4. The algorithm loads:
   - Complete items until the truck reaches near capacity  
   - A fraction of the next best item if remaining capacity exists  

5. The system outputs:
   - Final **optimal load plan**  
   - **Total utility score**  
   - Interactive **visual chart**  

---

