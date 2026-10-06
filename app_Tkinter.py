import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

class EcommerceAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Commerce Intelligence Analyzer")
        self.root.geometry("1200x800")
        
        self.df = None
        
        # --- 1. Top Frame: Data Loading ---
        top_frame = tk.Frame(root, pady=10)
        top_frame.pack(fill="x")
        
        btn_load = tk.Button(top_frame, text="1. Load CSV File", command=self.load_csv, font=("Arial", 10, "bold"), bg="#4CAF50", fg="white")
        btn_load.pack(side="left", padx=10)
        
        btn_demo = tk.Button(top_frame, text="Or Load Demo Data", command=self.load_demo_data)
        btn_demo.pack(side="left", padx=10)
        
        self.lbl_status = tk.Label(top_frame, text="No data loaded.", fg="red")
        self.lbl_status.pack(side="left", padx=20)
        
        # --- 2. Middle Frame: Column Mapping ---
        map_frame = tk.LabelFrame(root, text="2. Map Your Data", pady=5, padx=5)
        map_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(map_frame, text="Revenue/Spend Column:").grid(row=0, column=0, padx=5)
        self.cb_revenue = ttk.Combobox(map_frame, state="readonly")
        self.cb_revenue.grid(row=0, column=1, padx=5)
        
        tk.Label(map_frame, text="Category/Segment Column:").grid(row=0, column=2, padx=5)
        self.cb_category = ttk.Combobox(map_frame, state="readonly")
        self.cb_category.grid(row=0, column=3, padx=5)
        
        tk.Label(map_frame, text="Engagement Column (e.g., Visits):").grid(row=0, column=4, padx=5)
        self.cb_engagement = ttk.Combobox(map_frame, state="readonly")
        self.cb_engagement.grid(row=0, column=5, padx=5)
        
        btn_analyze = tk.Button(map_frame, text="3. Run Analysis", command=self.run_analysis, font=("Arial", 10, "bold"), bg="#2196F3", fg="white")
        btn_analyze.grid(row=0, column=6, padx=20)
        
        # --- 3. Bottom Frame: Results (Text + Graphs) ---
        results_frame = tk.Frame(root)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Text Box for KPIs and Theory
        self.txt_report = tk.Text(results_frame, height=15, font=("Consolas", 10), bg="#f4f4f4")
        self.txt_report.pack(fill="x", pady=5)
        
        # Canvas for Matplotlib Figures
        self.canvas_frame = tk.Frame(results_frame)
        self.canvas_frame.pack(fill="both", expand=True)
        self.canvas_widget = None

    def load_demo_data(self):
        """Generates synthetic data for quick testing."""
        np.random.seed(42)
        data = {
            'CustomerID': range(1, 201),
            'Total_Spend': np.random.uniform(20, 3000, 200).round(2),
            'Category': np.random.choice(['Electronics', 'Apparel', 'Home', 'Beauty', 'Sports'], 200, p=[0.35, 0.25, 0.2, 0.1, 0.1]),
            'Website_Visits': np.random.randint(1, 100, 200)
        }
        self.df = pd.DataFrame(data)
        self.update_dropdowns()
        self.lbl_status.config(text="Demo data loaded successfully.", fg="green")

    def load_csv(self):
        """Opens a file dialog to load any CSV."""
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filepath:
            try:
                self.df = pd.read_csv(filepath)
                self.df.columns = self.df.columns.str.strip()
                self.update_dropdowns()
                self.lbl_status.config(text=f"Loaded: {filepath.split('/')[-1]}", fg="green")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file:\n{e}")

    def update_dropdowns(self):
        """Detects numeric and categorical columns and populates dropdowns."""
        if self.df is not None:
            numeric_cols = self.df.select_dtypes(include=np.number).columns.tolist()
            cat_cols = self.df.select_dtypes(exclude=np.number).columns.tolist()
            
            if not numeric_cols or not cat_cols:
                messagebox.showerror("Data Error", "CSV must have at least one numeric and one text column.")
                return

            self.cb_revenue['values'] = numeric_cols
            self.cb_engagement['values'] = numeric_cols
            self.cb_category['values'] = cat_cols
            
            # Set defaults
            self.cb_revenue.current(0)
            self.cb_category.current(0)
            self.cb_engagement.current(min(1, len(numeric_cols)-1))

    def run_analysis(self):
        """Processes data, writes the text report, and draws charts."""
        if self.df is None:
            messagebox.showwarning("Warning", "Please load data first.")
            return
            
        val_col = self.cb_revenue.get()
        cat_col = self.cb_category.get()
        eng_col = self.cb_engagement.get()
        
        if not val_col or not cat_col or not eng_col:
            messagebox.showwarning("Warning", "Please select all columns.")
            return

        # --- Calculate Metrics ---
        total_revenue = self.df[val_col].sum()
        avg_order = self.df[val_col].mean()
        category_totals = self.df.groupby(cat_col)[val_col].sum().sort_values(ascending=False)
        top_cat = category_totals.index[0]
        top_cat_pct = (category_totals.iloc[0] / total_revenue) * 100
        correlation = self.df[eng_col].corr(self.df[val_col])

        # --- Generate Text Report ---
        self.txt_report.delete(1.0, tk.END)
        report = f"""{'='*60}
EXECUTIVE KPI SUMMARY
{'='*60}
Total Revenue Analyzed: ${total_revenue:,.2f}
Average Value per Customer: ${avg_order:,.2f}
Top Performing Segment: {top_cat} ({top_cat_pct:.1f}% of Total Revenue)

BUSINESS THEORY 1: The Pareto Principle (Category Contribution)
In e-commerce, identifying 'cash cow' segments ensures optimal marketing spend.
Segment Breakdown:
"""
        for cat, val in category_totals.items():
            pct = (val / total_revenue) * 100
            report += f" - {cat}: {pct:.1f}% (${val:,.2f})\n"

        report += f"""
BUSINESS THEORY 2: Intent vs. Browsing Behavior
Correlation between {eng_col} and {val_col}: {correlation:.2f}
"""
        if correlation > 0.5:
            report += "INSIGHT: Strong Positive Correlation. Higher engagement strongly drives higher spend.\n"
        elif correlation > 0.1:
            report += "INSIGHT: Weak Correlation. Engagement leads to some sales, but indicates window shopping.\n"
        else:
            report += "INSIGHT: Poor Correlation. More visits do not equate to higher spend. Investigate pricing or site friction.\n"
            
        self.txt_report.insert(tk.END, report)

        # --- Generate Charts (Embedded Matplotlib) ---
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()
            
        sns.set_theme(style="whitegrid")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        
        # Chart 1: Donut Chart
        colors = sns.color_palette('pastel')[0:len(category_totals)]
        ax1.pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%', 
                colors=colors, startangle=90, pctdistance=0.85, 
                wedgeprops=dict(width=0.4, edgecolor='w'))
        ax1.set_title(f"Revenue by {cat_col}", fontsize=12)
        
        # Chart 2: Scatter Plot
        sns.scatterplot(x=eng_col, y=val_col, hue=cat_col, data=self.df, palette='Set2', alpha=0.7, ax=ax2)
        z = np.polyfit(self.df[eng_col].dropna(), self.df[val_col].dropna(), 1)
        p = np.poly1d(z)
        ax2.plot(self.df[eng_col], p(self.df[eng_col]), "r--", alpha=0.5, label="Trendline")
        ax2.set_title(f"Engagement vs. Spend")
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
        
        plt.tight_layout()
        
        # Embed in Tkinter
        self.canvas_widget = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = EcommerceAnalyzerApp(root)
    root.mainloop()