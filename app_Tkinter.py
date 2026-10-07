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
        self.root.geometry("1250x850")
        self.root.configure(bg="#F0F4F8")
        
        self.df = None
        self.setup_styles()
        
        # --- 1. Header Banner ---
        header_frame = tk.Frame(root, bg="#1A365D", pady=15)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="📊 E-Commerce Customer Behavior Dashboard", 
                 font=("Segoe UI", 18, "bold"), bg="#1A365D", fg="white").pack()

        # --- 2. Top Control Panel (Cards) ---
        control_frame = tk.Frame(root, bg="#F0F4F8", pady=10, padx=20)
        control_frame.pack(fill="x")
        
        action_card = tk.Frame(control_frame, bg="white", padx=15, pady=15, relief="flat", highlightbackground="#E2E8F0", highlightthickness=1)
        action_card.pack(side="left", fill="y", padx=(0, 10))
        
        tk.Label(action_card, text="1. Load Data", font=("Segoe UI", 11, "bold"), bg="white", fg="#2D3748").pack(anchor="w", pady=(0, 5))
        
        btn_frame = tk.Frame(action_card, bg="white")
        btn_frame.pack()
        
        btn_load = tk.Button(btn_frame, text="📁 Upload CSV", command=self.load_csv, font=("Segoe UI", 10, "bold"), bg="#3182CE", fg="white", relief="flat", padx=15, pady=5, cursor="hand2")
        btn_load.pack(side="left", padx=(0, 10))
        
        btn_demo = tk.Button(btn_frame, text="🧪 Use Demo Data", command=self.load_demo_data, font=("Segoe UI", 10), bg="#E2E8F0", fg="#2D3748", relief="flat", padx=15, pady=5, cursor="hand2")
        btn_demo.pack(side="left")
        
        self.lbl_status = tk.Label(action_card, text="No data loaded.", bg="white", fg="#E53E3E", font=("Segoe UI", 9))
        self.lbl_status.pack(anchor="w", pady=(5, 0))
        
        map_card = tk.Frame(control_frame, bg="white", padx=15, pady=15, relief="flat", highlightbackground="#E2E8F0", highlightthickness=1)
        map_card.pack(side="left", fill="both", expand=True)
        
        tk.Label(map_card, text="2. Map Your Data", font=("Segoe UI", 11, "bold"), bg="white", fg="#2D3748").grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 10))
        
        tk.Label(map_card, text="Revenue Column:", bg="white", font=("Segoe UI", 9)).grid(row=1, column=0, padx=(0, 5), sticky="w")
        self.cb_revenue = ttk.Combobox(map_card, state="readonly", width=15)
        self.cb_revenue.grid(row=1, column=1, padx=(0, 15))
        
        tk.Label(map_card, text="Category Column:", bg="white", font=("Segoe UI", 9)).grid(row=1, column=2, padx=(0, 5), sticky="w")
        self.cb_category = ttk.Combobox(map_card, state="readonly", width=15)
        self.cb_category.grid(row=1, column=3, padx=(0, 15))
        
        tk.Label(map_card, text="Engagement (Visits):", bg="white", font=("Segoe UI", 9)).grid(row=1, column=4, padx=(0, 5), sticky="w")
        self.cb_engagement = ttk.Combobox(map_card, state="readonly", width=15)
        self.cb_engagement.grid(row=1, column=5, padx=(0, 15))
        
        btn_analyze = tk.Button(map_card, text="▶ Run Analysis", command=self.run_analysis, font=("Segoe UI", 10, "bold"), bg="#38A169", fg="white", relief="flat", padx=15, pady=3, cursor="hand2")
        btn_analyze.grid(row=1, column=6, padx=(10, 0))
        
        # --- 3. Notebook (Tabs) ---
        tab_frame = tk.Frame(root, bg="#F0F4F8", padx=20, pady=10)
        tab_frame.pack(fill="both", expand=True)
        
        self.notebook = ttk.Notebook(tab_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Tab 1: Report View
        self.tab_report = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_report, text="  📊 Report & Charts  ")
        
        self.txt_report = tk.Text(self.tab_report, height=8, font=("Consolas", 11), bg="#2D3748", fg="#F7FAFC", relief="flat", padx=15, pady=15)
        self.txt_report.pack(fill="x", padx=15, pady=15)
        
        self.canvas_frame = tk.Frame(self.tab_report, bg="white")
        self.canvas_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.canvas_widget = None

        # Tab 2: Data View
        self.tab_data = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_data, text="  🗃️ Raw Data Table  ")
        
        tk.Label(self.tab_data, text="💡 Double-click any row below to view the individual customer's profile. (Showing top 1,000 rows for performance)", bg="white", fg="#4A5568", font=("Segoe UI", 9, "italic")).pack(anchor="w", padx=10, pady=5)
        
        scroll_y = ttk.Scrollbar(self.tab_data, orient="vertical")
        scroll_x = ttk.Scrollbar(self.tab_data, orient="horizontal")
        
        self.tree = ttk.Treeview(self.tab_data, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, style="Custom.Treeview")
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)
        
        self.tree.tag_configure('evenrow', background="#F7FAFC")
        self.tree.tag_configure('oddrow', background="#FFFFFF")
        self.tree.bind("<Double-1>", self.show_customer_profile)

    def setup_styles(self):
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
            
        style.configure("TNotebook", background="#F0F4F8", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[15, 5], background="#E2E8F0", foreground="#2D3748")
        style.map("TNotebook.Tab", background=[("selected", "white")], foreground=[("selected", "#3182CE")])
        
        style.configure("Custom.Treeview", font=("Segoe UI", 9), rowheight=25, borderwidth=0)
        style.configure("Custom.Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#E2E8F0", foreground="#2D3748")
        style.map("Custom.Treeview.Heading", background=[('active', '#CBD5E0')])

    def show_customer_profile(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_data = self.tree.item(selected_item[0], "values")
        columns = self.tree["columns"]

        pop = tk.Toplevel(self.root)
        pop.title("Customer Profile")
        pop.geometry("350x450")
        pop.configure(bg="#F0F4F8")
        pop.resizable(False, False)
        pop.transient(self.root)
        pop.grab_set()

        header = tk.Frame(pop, bg="#3182CE", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="👤 Customer Profile", font=("Segoe UI", 14, "bold"), bg="#3182CE", fg="white").pack()

        card = tk.Frame(pop, bg="white", padx=20, pady=20, relief="flat", highlightbackground="#E2E8F0", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        for i, (col, val) in enumerate(zip(columns, item_data)):
            tk.Label(card, text=f"{col}:", font=("Segoe UI", 10, "bold"), bg="white", fg="#4A5568").grid(row=i, column=0, sticky="w", pady=8, padx=(0, 10))
            tk.Label(card, text=str(val), font=("Segoe UI", 10), bg="white", fg="#2D3748").grid(row=i, column=1, sticky="w", pady=8)

        btn_close = tk.Button(pop, text="Close", command=pop.destroy, font=("Segoe UI", 10), bg="#E2E8F0", fg="#2D3748", relief="flat", padx=20, pady=5, cursor="hand2")
        btn_close.pack(pady=(0, 20))

    def load_demo_data(self):
        np.random.seed(42)
        data = {
            'CustomerID': range(1, 201),
            'Age': np.random.randint(18, 70, 200),
            'Total_Spend': np.random.uniform(20, 3000, 200).round(2),
            'Items_Purchased': np.random.randint(1, 30, 200),
            'Category': np.random.choice(['Electronics', 'Apparel', 'Home', 'Beauty', 'Sports'], 200, p=[0.35, 0.25, 0.2, 0.1, 0.1]),
            'Website_Visits': np.random.randint(1, 100, 200)
        }
        self.df = pd.DataFrame(data)
        self.update_dropdowns()
        # Removed auto-run and data population to prevent lag
        self.lbl_status.config(text="✓ Demo data loaded. Select columns and run.", fg="#38A169")

    def load_csv(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filepath:
            try:
                self.df = pd.read_csv(filepath)
                self.df.columns = self.df.columns.str.strip()
                self.update_dropdowns()
                # Removed auto-run and data population to prevent lag
                self.lbl_status.config(text=f"✓ Loaded: {filepath.split('/')[-1]}", fg="#38A169")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file:\n{e}")

    def update_dropdowns(self):
        if self.df is not None:
            numeric_cols = self.df.select_dtypes(include=np.number).columns.tolist()
            cat_cols = self.df.select_dtypes(exclude=np.number).columns.tolist()
            
            if not numeric_cols or not cat_cols:
                messagebox.showerror("Data Error", "CSV must have at least one numeric and one text column.")
                return

            self.cb_revenue['values'] = numeric_cols
            self.cb_engagement['values'] = numeric_cols
            self.cb_category['values'] = cat_cols
            
            self.cb_revenue.current(0)
            self.cb_category.current(0)
            self.cb_engagement.current(min(1, len(numeric_cols)-1))

    def populate_data_viewer(self):
        self.tree.delete(*self.tree.get_children())
        if self.df is not None:
            self.tree["columns"] = list(self.df.columns)
            self.tree["show"] = "headings"
            
            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, anchor="center")
            
            # Performance fix: Cap the Treeview to 1000 rows
            preview_df = self.df.head(1000)
            for index, row in preview_df.iterrows():
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=list(row), tags=(tag,))

    def run_analysis(self):
        if self.df is None: 
            messagebox.showwarning("Warning", "Please load a CSV file first.")
            return
        
        val_col, cat_col, eng_col = self.cb_revenue.get(), self.cb_category.get(), self.cb_engagement.get()
        if not val_col or not cat_col or not eng_col: 
            messagebox.showwarning("Warning", "Please select all mapping columns.")
            return

        # Populate the Excel view ONLY after the user clicks run
        self.populate_data_viewer()

        total_revenue = self.df[val_col].sum()
        avg_order = self.df[val_col].mean()
        category_totals = self.df.groupby(cat_col)[val_col].sum().sort_values(ascending=False)
        top_cat = category_totals.index[0]
        correlation = self.df[eng_col].corr(self.df[val_col])

        self.txt_report.delete(1.0, tk.END)
        report = f" KPI SUMMARY: Total Revenue: ${total_revenue:,.2f}  |  Avg Value: ${avg_order:,.2f}  |  Top Segment: {top_cat}\n"
        report += "-"*100 + "\n"
        report += f" 📈 PARETO BREAKDOWN (Revenue by {cat_col}):\n"
        for cat, val in category_totals.items():
            pct = (val / total_revenue) * 100
            report += f"    • {cat.ljust(15)} : {pct:>5.1f}%  (${val:,.2f})\n"

        report += f"\n 🔍 BEHAVIORAL INSIGHT (Correlation = {correlation:.2f}):\n    "
        if correlation > 0.5: report += "STRONG POSITIVE: High engagement is successfully driving high conversions."
        elif correlation > 0.1: report += "WEAK POSITIVE: High visits show interest, but indicate 'window shopping' behavior."
        else: report += "POOR CORRELATION: Engagement does not lead to sales. Review pricing/site friction."
            
        self.txt_report.insert(tk.END, report)

        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()
            
        sns.set_theme(style="white", palette="muted")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor='white')
        
        colors = sns.color_palette('pastel')[0:len(category_totals)]
        ax1.pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%', 
                colors=colors, startangle=90, pctdistance=0.85, 
                wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
        ax1.set_title(f"Revenue Contribution by {cat_col}", fontsize=12, pad=15, fontweight='bold', color="#2D3748")
        
        sns.scatterplot(x=eng_col, y=val_col, hue=cat_col, data=self.df, palette='Set2', alpha=0.8, ax=ax2, s=60, edgecolor=None)
        z = np.polyfit(self.df[eng_col].dropna(), self.df[val_col].dropna(), 1)
        p = np.poly1d(z)
        ax2.plot(self.df[eng_col], p(self.df[eng_col]), color="#E53E3E", linestyle="--", alpha=0.7)
        ax2.set_title("Customer Intent (Engagement vs. Spend)", fontsize=12, pad=15, fontweight='bold', color="#2D3748")
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
        sns.despine(ax=ax2)
        
        plt.tight_layout()
        
        self.canvas_widget = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(fill="both", expand=True)
        self.notebook.select(self.tab_report)

if __name__ == "__main__":
    root = tk.Tk()
    app = EcommerceAnalyzerApp(root)
    root.mainloop()