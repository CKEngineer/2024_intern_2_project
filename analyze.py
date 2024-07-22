import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
from main import filtered_df,root


def analyze_data():
    try:
        if filtered_df is not None:
            # Create a new window for data analysis
            analysis_window = tk.Toplevel(root)
            analysis_window.title("Data Analysis")
            analysis_window.geometry("800x600")

            # Create a notebook widget for tabbed interface
            notebook = ttk.Notebook(analysis_window)
            notebook.pack(fill=tk.BOTH, expand=True)

            # Create frames for each tab
            head_frame = ttk.Frame(notebook)
            describe_frame = ttk.Frame(notebook)
            detailed_stats_frame = ttk.Frame(notebook)
            columns_frame = ttk.Frame(notebook)

            # Add tabs to the notebook
            notebook.add(head_frame, text="First 5 Rows")
            notebook.add(describe_frame, text="Summary Statistics")
            notebook.add(detailed_stats_frame, text="Detailed Stats")
            notebook.add(columns_frame, text="Column Names")

            # Create a canvas widget to enable scrolling for each frame
            def create_scrollable_canvas(parent_frame):
                try:
                    canvas = tk.Canvas(parent_frame)
                    vsb = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
                    hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=canvas.xview)
                    scroll_frame = ttk.Frame(canvas)

                    canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
                    vsb.pack(side=tk.RIGHT, fill=tk.Y)
                    hsb.pack(side=tk.BOTTOM, fill=tk.X)
                    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

                    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

                    return scroll_frame
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while creating scrollable canvas: {e}")

            # Display the first 5 rows of the database through df.head()
            head_scroll_frame = create_scrollable_canvas(head_frame)
            head_tree = ttk.Treeview(head_scroll_frame)
            head_tree["columns"] = list(filtered_df.columns)
            head_tree["show"] = "headings"
            for column in head_tree["columns"]:
                head_tree.heading(column, text=column)
            for index, row in filtered_df.head().iterrows():
                head_tree.insert("", "end", values=list(row))
            head_tree.pack(pady=5, fill=tk.BOTH, expand=True)

            # Display df.describe()
            describe_scroll_frame = create_scrollable_canvas(describe_frame)
            describe_tree = ttk.Treeview(describe_scroll_frame)
            describe_data = filtered_df.describe()
            describe_tree["columns"] = list(describe_data.columns)
            describe_tree["show"] = "headings"
            for column in describe_tree["columns"]:
                describe_tree.heading(column, text=column)
            for index, row in describe_data.iterrows():
                describe_tree.insert("", "end", values=list(row))
            describe_tree.pack(pady=5, fill=tk.BOTH, expand=True)

            # Display more detailed summary statistics
            detailed_stats_scroll_frame = create_scrollable_canvas(detailed_stats_frame)
            numeric_df = filtered_df.select_dtypes(include=[float, int])  # Select only numeric columns
            detailed_stats = {
                "Mean": numeric_df.mean(),
                "Median": numeric_df.median(),
                "Mode": numeric_df.mode().iloc[0],  # Mode can have multiple values, taking the first one
                "Standard Deviation": numeric_df.std(),
                "Variance": numeric_df.var(),
                "Min": numeric_df.min(),
                "Max": numeric_df.max(),
                "25th Percentile": numeric_df.quantile(0.25),
                "50th Percentile (Median)": numeric_df.quantile(0.5),
                "75th Percentile": numeric_df.quantile(0.75)
            }

            for stat_name, stat_values in detailed_stats.items():
                stat_label = tk.Label(detailed_stats_scroll_frame, text=f"{stat_name}:\n{stat_values}\n")
                stat_label.pack(pady=5, anchor="w")

            # Display column names
            columns_scroll_frame = create_scrollable_canvas(columns_frame)
            columns_label = tk.Label(columns_scroll_frame, text="Column Names:\n" + "\n".join(filtered_df.columns))
            columns_label.pack(pady=5, anchor="w")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred in analyze_data function: {e}")