# Disaster Relief Optimization – Fractional Knapsack

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?style=for-the-badge&logo=pandas)
![Plotly](https://img.shields.io/badge/Charts-Plotly-3F4F75?style=for-the-badge&logo=plotly)

---

## Overview

This project implements a **Fractional Knapsack–based optimization tool** to assist in planning and managing disaster-relief logistics.  
It helps determine how to **maximize the utility of relief items** when truck capacity is limited.  
The system is built using **Streamlit**, enabling real-time interaction, visualization, and CSV integration.

The tool is designed for agencies that need **efficient decision-making**, particularly during emergency supply distribution.

---

## Features

- Supports **manual entry** and **CSV upload** for items  
- Applies **Fractional Knapsack Algorithm** to compute optimal loading  
- Generates a detailed **load plan table**  
- Provides total utility score  
- Interactive **Plotly bar chart** for visualization  
- Clean Streamlit UI with centered action components  
- Works for any number of items and capacities  

---

## Tech Stack

| Component | Technology | Purpose |
|----------|------------|---------|
| **Frontend Framework** | Streamlit | UI, forms, layout, interactions |
| **Backend Logic** | Python | Core computation and data processing |
| **Data Handling** | Pandas | Reading, structuring, and transforming item data |
| **Visualization** | Plotly Express | Interactive charts for load distribution |
| **Deployment Ready** | Streamlit Cloud / Local | One-click deployment support |

---

## How It Works

1. The user submits relief item data (name, weight, importance).  
2. The system calculates **importance-to-weight ratio**.  
3. Items are sorted in descending order of utility density.  
4. The algorithm fills the truck with:
   - Full items if capacity allows  
   - Fraction of the next item if capacity remains  
5. Final load plan and utility are displayed along with a visualization.

---

