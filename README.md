# 🛒 E-Commerce Customer Behavior Analyzer

A modern, Python-based desktop application that ingests raw e-commerce customer data and transforms it into actionable business intelligence. Built for a Python programming laboratory, this tool features a Power BI-style tabbed interface, dynamic column mapping, and integrated statistical visualizations.

## ✨ Features

* **Dynamic Data Ingestion:** Upload any standard CSV dataset. The app automatically detects numeric and categorical columns.
* **Synthetic Data Fallback:** Includes a built-in demo data generator for instant testing and academic demonstrations without needing an external file.
* **Power BI-Style Interface:** 
  * **Report View:** Displays executive KPIs, a terminal-style business insights log, a Pareto (donut) chart, and a regression (scatter) plot.
  * **Data View:** Features a scrollable, striped-row spreadsheet viewer to inspect the raw data.
* **Business Intelligence Metrics:**
  * **The Pareto Principle (80/20 Rule):** Automatically groups and visualizes revenue contribution by product category.
  * **Intent vs. Browsing Behavior:** Calculates the Pearson correlation between customer engagement (e.g., website visits) and conversions (total spend) to identify "window shopping" trends.
* **Modern UI/UX:** Built with Tkinter's `ttk` engine, featuring a clean white/slate color palette, flat buttons, and seamless Matplotlib chart integration.

## 🛠️ Technology Stack

* **Language:** Python 3.8+
* **GUI Framework:** Tkinter (Standard Library)
* **Data Processing:** Pandas, NumPy
* **Data Visualization:** Matplotlib, Seaborn

## 🚀 Installation & Setup

1. **Clone or Download the Repository**
   Ensure all project files (including `app_Tkinter.py`) are in a single directory.

2. **Install Python Dependencies**
   Open your terminal or command prompt and install the required data science libraries:
   ```bash
   pip install pandas numpy matplotlib seaborn