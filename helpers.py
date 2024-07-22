import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

def add_scrollbars(frame, widget):
    try:
        vsb = ttk.Scrollbar(frame, orient="vertical", command=widget.yview)
        vsb.pack(side='right', fill='y')
        widget.configure(yscrollcommand=vsb.set)
        
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=widget.xview)
        hsb.pack(side='bottom', fill='x')
        widget.configure(xscrollcommand=hsb.set)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while adding scrollbars: {e}")

def save_data(par_dataframe):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        par_dataframe.to_csv(file_path, index=False)
        messagebox.showinfo("File Saved", f"File has been saved as {file_path}")

def save_filtered_data(filtered_df):
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            filtered_df.to_csv(file_path, index=False)
            messagebox.showinfo("File Saved", f"Filtered data has been saved as {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving filtered data: {e}")
