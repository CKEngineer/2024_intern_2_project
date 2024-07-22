import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
from main import df,root
from filter_operations import display_filtered_data


def project_columns():
    if df is not None:
        project_window = tk.Toplevel(root)
        project_window.title("Project Columns")
        project_window.geometry("400x300")
        
        tk.Label(project_window, text="Select Columns (comma separated)").pack(pady=5)
        column_entry = tk.Entry(project_window)
        column_entry.pack(pady=5)

        def apply_projection():
            columns = column_entry.get().split(',')
            columns = [col.strip() for col in columns]
            if columns:
                global filtered_df
                filtered_df = df.loc[:, columns]
                display_filtered_data(filtered_df)
                project_window.destroy()

        apply_button = tk.Button(project_window, text="Apply Projection", command=apply_projection)
        apply_button.pack(pady=10)